import argparse
import sys
import traceback
from pathlib import Path
from shutil import rmtree

from .exceptions import ClientException
from .site import Site


def main():
    parser = argparse.ArgumentParser(prog='gilbert', description="Gilbert static site generator")
    parser.add_argument('--root', '-r', type=Path, default=Path.cwd(),
                        help="Root of site data [defaults to CWD]")
    parser.add_argument('--debug', '-d', default=False, action="store_true",
                        help="Additional debugging [defaults to off]")
    parser.add_argument('action', choices=[
        'init',
        'render',
        'watch',
        'plugins',
        'clean',
    ])

    args = parser.parse_args()

    site = Site(args.root)

    try:
        if args.action == 'init':
            site.init()
        elif args.action == 'render':
            site.render()
        elif args.action == 'watch':
            site.watch()
        elif args.action == 'plugins':
            from .content import Content
            print("")
            print("File extensions:")
            print(f"  {', '.join(site.__loaders__)}")
            print("")
            print("Content Types:")
            for name in Content._types:
                print(f"- {name}")
            print("")
        elif args.action == 'clean':
            def onerror(func, path, exc_info):
                print(f"!! Unable to remove {path}")

            for child in site.dest_dir.iterdir():
                if child.is_dir():
                    rmtree(child, onerror=onerror)
                else:
                    try:
                        child.unlink()
                    except Exception:
                        onerror(None, str(child), None)

    except ClientException as exc:
        if args.debug:
            traceback.print_exc(file=sys.stdout)
        else:
            print(exc)
