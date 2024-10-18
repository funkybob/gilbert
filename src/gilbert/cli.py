import argparse
import sys
import traceback
from pathlib import Path
from shutil import rmtree

from .exceptions import ClientError
from .site import Site

parser = argparse.ArgumentParser(prog="gilbert", description="Gilbert static site generator")
parser.add_argument(
    "--root",
    "-r",
    type=Path,
    default=Path.cwd(),
    help="Root of site data [defaults to CWD]",
)
parser.add_argument(
    "--debug",
    "-d",
    default=False,
    action="store_true",
    help="Additional debugging [defaults to off]",
)

parser.set_defaults(func=None)

subparsers = parser.add_subparsers()


def subcommand(name):
    # TODO: Add option to add extra arguments

    def _inner(handler):
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(func=handler)
        return handler

    return _inner


@subcommand("init")
def handle_init(_args, site):
    site.init()


@subcommand("render")
def handle_render(_args, site):
    site.render()


@subcommand("plugins")
def handle_plugins(_args, site):
    from .content import Content

    print("")
    print("File extensions:")
    print(f"  {', '.join(site.__loaders__)}")
    print("")
    print("Content Types:")
    for name in Content._types:
        print(f"- {name}")
    print("")


@subcommand("clean")
def handle_clean(_args, site):
    def onerror(_, path, __):
        print(f"!! Unable to remove {path}")

    for child in site.dest_dir.iterdir():
        if child.is_dir():
            rmtree(child, onerror=onerror)
        else:
            try:
                child.unlink()
            except Exception:
                onerror(None, str(child), None)


def handle_serve(args, site):
    import uvicorn

    from .server import make_app

    options = {
        "host": args.bind,
        "port": args.port,
    }

    app = make_app(site)

    uvicorn.run(app, **options)


subparser = subparsers.add_parser("serve")
subparser.add_argument(
    "--bind",
    "-b",
    default="127.0.0.1",
    metavar="ADDRESS",
    help="Specify alternate bind address [default: all interfaces]",
)
subparser.add_argument(
    "port",
    action="store",
    default=8000,
    type=int,
    nargs="?",
    help="Specify alternate port [default: 8000]",
)
subparser.set_defaults(func=handle_serve)


def main():
    args = parser.parse_args()

    if args.func is None:
        parser.print_help()
        return

    site = Site(args.root)

    try:
        args.func(args, site)
    except ClientError as exc:
        if args.debug:
            traceback.print_exc(file=sys.stdout)
        else:
            print(exc)
