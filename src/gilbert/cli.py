import argparse
import sys
import traceback
from pathlib import Path
from shutil import rmtree

from .exceptions import ClientException
from .site import Site

parser = argparse.ArgumentParser(prog="gilbert", description="Gilbert static site generator")
parser.add_argument("--root", "-r", type=Path, default=Path.cwd(), help="Root of site data [defaults to CWD]")
parser.add_argument("--debug", "-d", default=False, action="store_true", help="Additional debugging [defaults to off]")

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
def handle_init(args, site):
    site.init()


@subcommand("render")
def handle_render(args, site):
    site.render()


@subcommand("watch")
def handle_watch(args, site):
    import asyncio

    loop = asyncio.get_event_loop()

    loop.create_task(site.watch(loop))


@subcommand("plugins")
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


@subcommand("clean")
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


def handle_serve(args, site):

    from aiohttp import web

    def default_index(request):
        return web.Response(status=301, headers={"Location": "/index.html"})

    app = web.Application()
    app.router.add_route("GET", "/", default_index)
    app.router.add_static("/", site.dest_dir)

    if args.watch:
        handle_watch(args, site)

    web.run_app(app, host=args.bind, port=args.port)


subparser = subparsers.add_parser("serve")
subparser.add_argument(
    "--bind",
    "-b",
    default="0.0.0.0",
    metavar="ADDRESS",
    help="Specify alternate bind address [default: all interfaces]",
)
subparser.add_argument("--watch", "-w", default=False, action="store_true", help="Watch files and rebuild on changes")
subparser.add_argument(
    "port", action="store", default=8000, type=int, nargs="?", help="Specify alternate port [default: 8000]"
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
    except ClientException as exc:
        if args.debug:
            traceback.print_exc(file=sys.stdout)
        else:
            print(exc)
