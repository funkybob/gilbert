from collections import defaultdict
from importlib import import_module
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import yaml

from stencil import Context, TemplateLoader

from .collection import Collection
from .content import Page


class emits:
    def __init__(self, event):
        self.event = event

    def __call__(self, method):
        event = self.event

        def _inner(self, *args, **kwargs):
            self.emit(f"before-{event}")
            try:
                return method(self, *args, **kwargs)
            finally:
                self.emit(f"after-{event}")

        return _inner


class Site:
    """
    Configuration of main site.
    """

    __context_generators__: List[Callable[[Dict], Dict]] = []
    __loaders__: Dict[str, Callable[[Path], Tuple[str, Dict]]] = {}

    def __init__(self, root: Path):
        self.hooks: Dict[str, List[Callable[[Site], None]]] = defaultdict(list)

        self.root = root

        self.templates_dir = self.root / "templates"
        self.pages_dir = self.root / "pages"
        self.content_dir = self.root / "content"
        self.dest_dir = self.root / "docs"

        config_file = root / "config.yml"

        if config_file.is_file():
            self.config = yaml.load(config_file.open(), Loader=yaml.Loader)
        else:
            self.config = {}

        self.templates = TemplateLoader([self.templates_dir,])
        self.load_plugins()

        self.emit("init")

    # Event handling

    def on(self, event, handler):
        self.hooks[event].append(handler)

    def emit(self, event):
        for handler in self.hooks[event]:
            handler(self)

    # Actions

    def init(self):
        """
        Initialise directories.
        """
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.pages_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.dest_dir.mkdir(parents=True, exist_ok=True)

        (self.root / "config.yml").write_text(yaml.dump({"plugins": [], "global": {},}, Dumper=yaml.Dumper))

    def load_plugin(self, package_name):
        """
        Helper function for importing a plugin and handling its init.
        """
        try:
            module = import_module(package_name)
        except ImportError as e:
            print(f"Failed importing {package_name}: {e !r}")
            return False

        init_func = getattr(module, "init_site", None)
        if init_func:
            self.on("init", init_func)

        return True

    def load_plugins(self):
        for package_name in self.config.get("plugins", []):
            if self.load_plugin(package_name):
                print(f"Loaded plugin: {package_name}")

        if (self.root / "plugins.py").is_file() or (self.root / "plugins/__init__.py").is_file():
            import sys

            root_path = str(self.root)
            if root_path not in sys.path:
                sys.path.insert(0, root_path)
            if self.load_plugin("plugins"):
                print("Loaded local plugins.")

    @classmethod
    def register_loader(cls, ext, func):
        if ext in cls.__loaders__:
            print(f"WARNING: Overriding loader for {ext}")
        cls.__loaders__[ext] = func
        return func

    @classmethod
    def register_context_provider(cls, func):
        if func in cls.__context_generators__:
            raise Warning(f"Context generator {func} already registered.")
        cls.__context_generators__.append(func)
        return func

    @emits("render")
    def render(self):
        self.emit("before-render")
        self.load_content()
        self.load_pages()

        self.render_pages()
        self.emit("after-render")

    @emits("content")
    def load_content(self):
        self.content = Collection(self, loaders=self.__loaders__)
        self.content.load(self.content_dir)
        print(f"Found {len(self.content)} content objects.")

    @emits("pages")
    def load_pages(self):
        self.pages = Collection(self, default_type=Page, loaders=self.__loaders__)
        self.pages.load(self.pages_dir)
        print(f"Found {len(self.pages)} pages.")

    def render_pages(self):
        for name, page in sorted(self.pages.items()):
            print(f"Rendering {name} ...")
            page.render()
        print("-- Done.")

    def get_context(self, obj, **kwargs) -> Context:

        ctx = {
            "site": self,
            "pages": self.pages,
            "content": self.content,
            "this": obj,
            **self.config.get("global", {}),
            **kwargs,
        }

        for func in self.__context_generators__:
            ctx = func(ctx)

        return Context(ctx)

    async def watch(self, loop):
        """
        Watch for changes, then re-render
        """
        import aionotify

        watcher = aionotify.Watcher()

        for path in (self.templates_dir, self.pages_dir, self.content_dir):
            watcher.watch(str(path), flags=aionotify.Flags.MODIFY | aionotify.Flags.CREATE | aionotify.Flags.DELETE)

        await watcher.setup(loop)

        while True:
            await watcher.get_event()
            self.templates.clear()
            self.render()
