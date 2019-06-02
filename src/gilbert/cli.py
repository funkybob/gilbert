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


subparsers = parser.add_subparsers()


def handle_init(args, site):
    site.init()


init_parser = subparsers.add_parser('init')
init_parser.set_defaults(func=handle_init)


def handle_render(args, site):
    site.render()


render_parser = subparsers.add_parser('render')
render_parser.set_defaults(func=handle_render)


def handle_watch(args, site):
    site.watch()


watch_parser = subparsers.add_parser('watch')
watch_parser.set_defaults(func=handle_watch)


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


plugins_parser = subparsers.add_parser('plugins')
plugins_parser.set_defaults(func=handle_plugins)


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


clean_parser = subparsers.add_parser('clean')
clean_parser.set_defaults(func=handle_clean)


def handle_serve(args, site):
    import http.server
    from functools import partial
    http.server.test(
        partial(http.server.SimpleHTTPRequestHandler, directory=str(site.dest_dir))
    )


serve_parser = subparsers.add_parser('serve')
serve_parser.set_defaults(func=handle_serve)


def main():
    args = parser.parse_args()
    site = Site(args.root)

    try:
        args.func(args, site)
    except ClientException as exc:
        if args.debug:
            traceback.print_exc(file=sys.stdout)
        else:
            print(exc)
