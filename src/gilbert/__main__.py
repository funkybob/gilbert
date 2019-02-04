from pathlib import Path

from .site import Site

HERE = Path.cwd()


site = Site(HERE)

site.render()
