from typing import Optional, Dict, List, Any
import json, pandas, numpy, tempfile, sqlite3, logging, time, codecs
from modelbit.api import MbApi, DatasetApi
from modelbit.error import UserFacingError
from modelbit.utils import inDeployment
from modelbit.internal.secure_storage import getSecureData, DownloadableObjectInfo
from modelbit.internal.s3 import getS3FileBytes
from modelbit.internal.retry import retry

logger = logging.getLogger(__name__)

FilterType = Optional[Dict[str, List[Any]]]


def toUrlBranch(b: str):
  return b.replace("/", "~")


@retry(4, logger)
def _wrappedGetS3FileBytes(path: str):
  return getS3FileBytes(path)


@retry(4, logger)
def _wrappedGetSecureData(dri: DownloadableObjectInfo, desc: str) -> bytes:
  return getSecureData(dri, desc)


def downloadDecryptData(mbApi: MbApi, path: str, desc: str) -> Optional[bytes]:
  if inDeployment():
    return _wrappedGetS3FileBytes(path)
  else:
    return _downloadFromWeb(mbApi, path=path, desc=desc)


def _downloadFromWeb(mbApi: MbApi, path: str, desc: str) -> Optional[bytes]:
  dri = DatasetApi(mbApi).getDatasetPartDownloadInfo(path)
  if dri is None:
    raise UserFacingError(f"Failed finding download info for dataset part: {path}")
  return _wrappedGetSecureData(dri, desc)


class Shard:

  def __init__(self, mbApi: MbApi, params: Dict[str, Any], dsName: str, numShards: int):
    self.mbApi = mbApi
    self.dsName = dsName
    self.numShards = numShards
    self.shardId = params["shardId"]
    self.shardPath = params["shardPath"]
    self.shardColumn = params["shardColumn"]
    self.minValue = params["minValue"]
    self.maxValue = params["maxValue"]
    self.numBytes = params["numBytes"]
    self.numRows = params["numRows"]
    self.featureDbFile = tempfile.NamedTemporaryFile()
    self.completeDf: Optional[pandas.DataFrame] = None
    self.dbConn: Optional[sqlite3.Connection] = None

  def __del__(self):
    if self.dbConn is not None:
      self.dbConn.close()
    self.featureDbFile.close()

  def getDbConn(self) -> sqlite3.Connection:
    if self.dbConn is None:
      shardData = downloadDecryptData(self.mbApi, self.shardPath,
                                      f"{self.dsName} (part {self.shardId} of {self.numShards})")
      if shardData is None:
        raise Exception(f"FailedGettingShard path={self.shardPath}")
      self.featureDbFile.write(shardData)
      self.dbConn = sqlite3.connect(self.featureDbFile.name, check_same_thread=False)
    return self.dbConn

  def filterToDf(self, filters: FilterType) -> Optional[pandas.DataFrame]:
    if filters is None:
      return self.getCompleteDf()

    if self.canSkip(filters):
      return None

    filterGroups: List[str] = []
    filterParams: List[Any] = []
    for filterCol, filterValues in filters.items():
      filterGroup: List[str] = []
      for val in filterValues:
        filterGroup.append(f"`{filterCol}` = ?")
        filterParams.append(val)
      filterGroups.append(f'({" or ".join(filterGroup)})')
    sql = f"select * from df where {' and '.join(filterGroups)}"
    df = pandas.read_sql_query(sql=sql, params=filterParams, con=self.getDbConn())  # type: ignore
    self.convertDbNulls(df)
    return df

  def getCompleteDf(self) -> pandas.DataFrame:
    if self.completeDf is None:
      df = pandas.read_sql_query(sql="select * from df", con=self.getDbConn())  # type: ignore
      self.convertDbNulls(df)
      self.completeDf = df
    return self.completeDf

  def canSkip(self, filters: FilterType) -> bool:
    if filters is None:
      return False

    colNameCaseMap: Dict[str, str] = {}
    for fName in filters.keys():
      colNameCaseMap[fName.lower()] = fName
    if self.shardColumn.lower() not in colNameCaseMap:
      return False

    filterShardColCasedToFilters = colNameCaseMap[self.shardColumn.lower()]
    lastFilterVal: Any = None
    try:
      canSkip = True
      for filterVal in filters[filterShardColCasedToFilters]:
        lastFilterVal = filterVal
        if filterVal is None or self.minValue is None or self.maxValue is None:
          canSkip = False
        elif self.minValue <= filterVal <= self.maxValue:
          canSkip = False
      return canSkip
    except TypeError as err:
      if "<=" in str(err):
        comparison = " <= ".join([
            f"{type(self.minValue).__name__}({self.minValue})",
            f"{type(lastFilterVal).__name__}({lastFilterVal})",
            f"{type(self.maxValue).__name__}({self.maxValue})",
        ])
        raise UserFacingError(f"Invalid comparison when searching for feature, {comparison}. Error: {err}")
      raise err

  def convertDbNulls(self, df: pandas.DataFrame):
    df.replace(["\\N", "\\\\N"], numpy.nan, inplace=True)  # type: ignore


class FeatureStore:

  ManifestTimeoutSeconds = 5 * 60 if inDeployment() else 10

  def __init__(self, mbApi: MbApi, branch: str, dsName: str):
    self.mbApi = mbApi
    self.branch = branch
    self.dsName = dsName
    self.manifestPath: str = self.getManifestPath()
    self.manifestBytes: bytes = b""
    self.shards: List[Shard] = []
    self.manifestExpiresAt: float = 0

  def getManifestPath(self) -> str:
    return f'datasets/{self.dsName}/{toUrlBranch(self.branch)}.manifest'

  def maybeRefreshManifest(self):
    if len(self.manifestBytes) > 0 and time.time() < self.manifestExpiresAt:
      return
    newManifestBytes: Optional[bytes] = None
    notFoundError = UserFacingError(f"Dataset not found: {self.branch}/{self.dsName}")
    try:
      newManifestBytes = downloadDecryptData(self.mbApi, self.manifestPath, f"{self.dsName} (index)")
    except UserFacingError as err:
      raise err
    except Exception as err:
      raise UserFacingError(f"Unable to fetch dataset {self.branch}/{self.dsName}: {err}")
    if newManifestBytes is None:
      raise notFoundError
    if newManifestBytes != self.manifestBytes:
      newManifestData: Dict[str, Any] = json.loads(codecs.decode(newManifestBytes))
      shardInfo: List[Dict[str, Any]] = newManifestData["shards"]
      self.shards = [
          Shard(self.mbApi, params=d, dsName=self.dsName, numShards=len(shardInfo)) for d in shardInfo
      ]
      self.manifestBytes = newManifestBytes
    self.manifestExpiresAt = time.time() + self.ManifestTimeoutSeconds

  def getDataFrame(self, filters: FilterType) -> pandas.DataFrame:
    self.maybeRefreshManifest()
    shardResults = [s.filterToDf(filters) for s in self.shards]
    shardResults = [s for s in shardResults if s is not None]
    if len(shardResults) == 0:
      firstDf = self.shards[0].getCompleteDf()
      assert firstDf is not None
      return firstDf.head(0)  # return empty df, not None, when filters match nothing
    return pandas.concat(shardResults)  #type: ignore


class FeatureStoreManager:

  def __init__(self, mbApi: MbApi):
    self.mbApi = mbApi
    self.featureStores: Dict[str, FeatureStore] = {}

  def getFeatureStore(self, branch: str, dsName: str) -> FeatureStore:
    lookupKey = f"{branch}/${dsName}"
    if lookupKey not in self.featureStores:
      self.featureStores[lookupKey] = FeatureStore(mbApi=self.mbApi, branch=branch, dsName=dsName)
    return self.featureStores[lookupKey]


_featureStoreManager: Optional[FeatureStoreManager] = None


def _getFeatureStoreManager(mbApi: MbApi) -> FeatureStoreManager:
  global _featureStoreManager
  if _featureStoreManager is None:
    _featureStoreManager = FeatureStoreManager(mbApi)
  return _featureStoreManager


def assertFilterFormat(filters: FilterType) -> None:
  if filters is None:
    return
  if type(filters) is not dict:
    raise UserFacingError(f"filters= must be None or a dictionary. It's currently a {type(filters)}")
  for k, v in filters.items():
    if type(k) is not str:
      raise UserFacingError(f"Filter keys must be strings. Found '{k}' which is a {type(v)}")
    if type(v) is not list:
      raise UserFacingError(f"Filter values must be lists. Found '{v}' which is a {type(v)}")


def getDataFrame(mbApi: MbApi, branch: str, dsName: str, filters: FilterType = None) -> pandas.DataFrame:
  if not inDeployment() and not mbApi.isAuthenticated():
    raise UserFacingError("Your session is not authenticated.")
  assertFilterFormat(filters)
  featureStore = _getFeatureStoreManager(mbApi).getFeatureStore(branch=branch, dsName=dsName)
  return featureStore.getDataFrame(filters)
