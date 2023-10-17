import argparse
import logging
import sys
from typing import Optional

from modelbit.error import ModelbitError

logger = logging.getLogger(__name__)


def cloneAction(target_folder: str, origin: Optional[str], **_) -> None:
  from modelbit.git.clone import clone
  clone(target_folder, origin=origin)


def versionAction(**_) -> None:
  from modelbit import __version__
  print(__version__)
  exit(0)


def cacheAction(command: str, workspace: Optional[str], **_) -> None:
  from modelbit.internal import cache
  if command == "clear":
    cache.clearCache(workspace)
  elif command == "list":
    from .. import ux
    headers = [
        ux.TableHeader("Workspace"),
        ux.TableHeader("Kind"),
        ux.TableHeader("Name"),
        ux.TableHeader("Size", alignment=ux.TableHeader.RIGHT)
    ]
    print(ux.renderTextTable(headers, cache.getCacheList(workspace), maxWidth=120))


def describeAction(filepath: Optional[str] = None, depth: int = 1, **_) -> None:
  from modelbit.internal.describe import calcHash, describeFile
  from modelbit.internal.file_stubs import toYaml

  if filepath is not None:
    with open(filepath, "rb") as f:
      content = f.read()
  else:
    content = sys.stdin.buffer.read()

  print(toYaml(calcHash(content), len(content), describeFile(content, depth)))


def gitfilterAction(**_) -> None:
  from modelbit.git.filter_process import process
  process()


def addPackageAction(pkgpath: str, force: bool, **_) -> None:
  from modelbit import add_package
  add_package(pkgpath, force)


def deletePackageAction(name: str, version: str, **_) -> None:
  from modelbit import delete_package
  delete_package(name, version)


def listPackageAction(name: Optional[str], **_) -> None:
  from modelbit import _mbApi
  from modelbit.internal.package import list_packages
  from .. import ux
  from modelbit.utils import timeago, sizeOfFmt
  headers = [
      ux.TableHeader("Name"),
      ux.TableHeader("Version"),
      ux.TableHeader("Added"),
      ux.TableHeader("Size", alignment=ux.TableHeader.RIGHT)
  ]
  pkgs = list_packages(name, _mbApi())
  if pkgs is None:
    return
  packageList = [[p.name, p.version, timeago(p.createdAtMs or 0), sizeOfFmt(p.size)] for p in pkgs]
  print(ux.renderTextTable(headers, packageList, maxWidth=120))


def initializeParser() -> argparse.ArgumentParser:
  visibleOptions: Optional[str] = '{clone,version,package}'
  if "-hh" in sys.argv:  # modelbit -hh to show full help
    visibleOptions = None
  parser = argparse.ArgumentParser(description="Modelbit CLI")
  subparsers = parser.add_subparsers(title='Actions', required=True, dest="action", metavar=visibleOptions)

  clone_parser = subparsers.add_parser('clone', help="Clone your Modelbit repository via git")
  clone_parser.set_defaults(func=cloneAction)
  clone_parser.add_argument('target_folder', nargs='?', default="modelbit")
  clone_parser.add_argument(
      '--origin',
      metavar='{modelbit,github,gitlab,etc}',
      required=False,
      help=
      'Repository to clone. Set to modelbit, github, or gitlab to specify the remote to use. If not set, will show an interactive prompt'
  )

  subparsers.add_parser('version', help="Display Modelbit package version").set_defaults(func=versionAction)

  cache_parser = subparsers.add_parser('cache')
  cache_parser.set_defaults(func=cacheAction)
  cache_parser.add_argument('command', choices=['list', 'clear'])
  cache_parser.add_argument('workspace', nargs='?')

  describe_parser = subparsers.add_parser('describe')
  describe_parser.set_defaults(func=describeAction)
  describe_parser.add_argument('filepath', nargs='?')
  describe_parser.add_argument('-d', '--depth', default=1, type=int)

  filter_parser = subparsers.add_parser('gitfilter')
  filter_parser.set_defaults(func=gitfilterAction)
  filter_parser.add_argument('command', choices=['process'])

  package_parser = subparsers.add_parser('package', help="Add private packages to Modelbit")

  pkg_sub_parser = package_parser.add_subparsers(title="command", required=True, dest="command")

  add_pkg_parser = pkg_sub_parser.add_parser("add", help="Upload a private package")
  add_pkg_parser.add_argument('pkgpath')
  add_pkg_parser.add_argument('-f', '--force', action='store_true', help="Clobber existing versions")
  add_pkg_parser.set_defaults(func=addPackageAction)

  list_pkg_parser = pkg_sub_parser.add_parser("list", help="List private packages")
  list_pkg_parser.add_argument('name', nargs='?')

  list_pkg_parser.set_defaults(func=listPackageAction)

  delete_pkg_parser = pkg_sub_parser.add_parser("delete", help="Delete private package")
  delete_pkg_parser.add_argument('name')
  delete_pkg_parser.add_argument('version')

  delete_pkg_parser.set_defaults(func=deletePackageAction)

  return parser


def processArgs() -> None:
  parser = initializeParser()
  args = parser.parse_args()
  try:
    args.func(**vars(args))
  except TypeError as e:
    # Catch wrong number of args
    logger.info("Bad command line", exc_info=e)
    parser.print_help()
  except KeyboardInterrupt:
    exit(1)
  except ModelbitError:
    # Already printed an error
    exit(1)
  except Exception as e:
    raise
