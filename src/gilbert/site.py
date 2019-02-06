from collections import OrderedDict
from importlib import import_module
from pathlib import Path

from stencil import Context, TemplateLoader

from .collection import Collection
from .content import Page


class Site:
    """
    Configuration of main site.
    """
    def __init__(self, root: Path):
        self.root = root

        self.templates_dir = self.root / 'templates'
        self.pages_dir = self.root / 'pages'
        self.content_dir = self.root / 'content'
        self.dest_dir = self.root / 'dist'

        self.templates = TemplateLoader([
            self.templates_dir,
        ])

    def init(self):
        """
        Initialise directories.
        """
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.pages_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.dest_dir.mkdir(parents=True, exist_ok=True)

    def load_plugins(self):
        from . import plugins

        found = OrderedDict()

        for path in plugins.__path__:
            root = Path(path)
            print(f"Searching {root} for plugins...")
            for child in root.iterdir():
                if not child.is_dir():
                    continue
                name = str(child.relative_to(root)).replace('/', '.')
                try:
                    import_module(f'gilbert.plugins.{name}')
                except ImportError:
                    continue
                else:
                    print(f'Loaded plugin: {name}')

        local_plugins =  self.root / 'plugins.py'
        if local_plugins.is_file():
            import sys
            root = str(self.root)
            if root not in sys.path:
                sys.path.insert(0, root)
            found['__local__'] = import_module('plugins')

        self.plugins = found

    def render(self):
        self.load_plugins()

        self.load_content()
        self.index_assets()
        self.render_pages()

    def load_content(self):
        self.content = Collection()
        self.content.load(self.root / 'content')

    def index_assets(self):
        pass

    def render_pages(self):
        self.pages = Collection(default_type=Page)
        self.pages.load(self.root / 'pages')

        for name, page in sorted(self.pages.items()):
            print(f"Rendering {name} ...")
            page.render(self)

    def get_context(self, obj, **kwargs) -> Context:
        return Context({
            'site': self,
            'pages': self.pages,
            'content': self.content,
            'this': obj,
            **kwargs
        })
