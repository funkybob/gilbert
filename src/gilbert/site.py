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

    __context_generators__ = []
    __loaders__ = {}

    def __init__(self, root: Path):
        self.root = root

        self.templates_dir = self.root / 'templates'
        self.pages_dir = self.root / 'pages'
        self.content_dir = self.root / 'content'
        self.dest_dir = self.root / 'docs'

        self.templates = TemplateLoader([
            self.templates_dir,
        ])
        self.load_plugins()

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
                if not (
                    child.is_dir() or (
                        child.is_file() and child.suffix == '.py'
                    )
                ) or child.name.startswith('__'):
                    continue

                rel_path = child.relative_to(root)

                name = '.'.join(rel_path.parts[:-1] + (rel_path.stem,))
                try:
                    import_module(f'gilbert.plugins.{name}')
                except ImportError as e:
                    print(f'Failed importing {name}: {e !r}')
                    continue
                else:
                    print(f'Loaded plugin: {name}')

        local_plugins = self.root / 'plugins.py'
        if local_plugins.is_file():
            import sys
            root = str(self.root)
            if root not in sys.path:
                sys.path.insert(0, root)
            found['__local__'] = import_module('plugins')

        self.plugins = found

    @classmethod
    def register_loader(cls, ext, func):
        if ext in cls.__loaders__:
            print(f"WARNING: Overriding loader for {ext}")
        cls.__loaders__[ext] = func
        return func

    @classmethod
    def register_context_provider(cls, func):
        if func in cls.__context_generators__:
            raise Warning(f'Context generator {func} already registered.')
        cls.__context_generators__.append(func)
        return func

    def render(self):
        self.load_content()
        self.load_pages()

        self.render_pages()

    def load_content(self):
        self.content = Collection(self, loaders=self.__loaders__)
        self.content.load(self.content_dir)
        print(f'Found {len(self.content)} content objects.')

    def load_pages(self):
        self.pages = Collection(self, default_type=Page, loaders=self.__loaders__)
        self.pages.load(self.pages_dir)
        print(f'Found {len(self.pages)} pages.')

    def render_pages(self):
        for name, page in sorted(self.pages.items()):
            print(f"Rendering {name} ...")
            page.render()

    def get_context(self, obj, **kwargs) -> Context:

        ctx = {
            'site': self,
            'pages': self.pages,
            'content': self.content,
            'this': obj,
            **kwargs
        }

        for func in self.__context_generators__:
            ctx = func(ctx)

        return Context(ctx)

    def watch(self):
        '''
        Watch for changes, then re-render
        '''
        import inotify.adapters
        from inotify.constants import IN_DELETE, IN_MOVE, IN_MODIFY
        i = inotify.adapters.InotifyTrees(
            [
                str(self.templates_dir),
                str(self.pages_dir),
                str(self.content_dir),
            ],
            mask=IN_DELETE | IN_MOVE | IN_MODIFY,
            block_duration_s=None,
        )

        for event in i.event_gen():
            if event is None:
                self.templates.clear()  # Reset template cache
                self.render()
