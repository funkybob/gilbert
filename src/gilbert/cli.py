import argparse
import sys
import traceback
from pathlib import Path
from shutil import rmtree

from .exceptions import ClientException
from .site import Site

parser = argparse.ArgumentParser(prog='gilbert', description="Gilbert static site generator")
parser.add_argument('--root', '-r', type=Path, default=Path.cwd(),
                    help="Root of site data [defaults to CWD]")
parser.add_argument('--debug', '-d', default=False, action="store_true",
                    help="Additional debugging [defaults to off]")

parser.set_defaults(func=None)

subparsers = parser.add_subparsers()


def subcommand(name):
    # TODO: Add option to add extra arguments

    def _inner(handler):
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(func=handler)
        return handler

    return _inner


@subcommand('init')
def handle_init(args, site):
    site.init()


@subcommand('render')
def handle_render(args, site):
    site.render()


@subcommand('watch')
def handle_watch(args, site):
    site.watch()


@subcommand('plugins')
def handle_plugins(args, site):
    from .content import Content
    print("")
    print("File extensions:")
    print(f"  {', '.join(site.__loaders__)}")
    print("")
    print("Content Types:")
    for name in Content._types:
        print(f"- {name}")
    print("")


@subcommand('clean')
def handle_clean(args, site):
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


@subcommand('serve')
def handle_serve(args, site):
    import http.server
    from functools import partial
    http.server.test(
        partial(http.server.SimpleHTTPRequestHandler, directory=str(site.dest_dir))
    )


def main():
    args = parser.parse_args()

    if args.func is None:
        parser.print_help()
        return

    site = Site(args.root)

    try:
        args.func(args, site)
    except ClientException as exc:
        if args.debug:
            traceback.print_exc(file=sys.stdout)
        else:
            print(exc)
