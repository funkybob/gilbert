from collections import defaultdict
from functools import wraps
from importlib import import_module
from pathlib import Path
from typing import Callable, Dict, List

import yaml
from stencil import Context, TemplateLoader

from .collection import Collection
from .content import Page
from .types import LoaderFunction, LoaderResult


class emits:
    """
    Method decorator to cause a method to emit before- and after- events.
    """

    def __init__(self, event: str):
        self.event = event

    def __call__(self, method: Callable) -> Callable:
        event = self.event

        @wraps(method)
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
    __loaders__: Dict[str, LoaderFunction] = {}

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

        self.templates = TemplateLoader([self.templates_dir])
        self.load_plugins()

        self.emit("init")

    # Event handling

    def on(self, event: str, handler: Callable[["Site"], None]) -> None:
        """
        Registers a callback function for a given event.
        """
        self.hooks[event].append(handler)

    def emit(self, event: str) -> None:
        """
        Emit a named event to all registered callbacks.
        """
        for handler in self.hooks[event]:
            handler(self)

    # Actions

    def init(self):
        """
        Create a new site root.

        Ensures the template, pages, content, and destination directories for this site exist, creating them if they don't.
        Creates an skeleton ``config.yml`` file.
        """
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.pages_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.dest_dir.mkdir(parents=True, exist_ok=True)

        (self.root / "config.yml").write_text(yaml.dump({"plugins": [], "global": {}}, Dumper=yaml.Dumper))

    def load_plugin(self, package_name: str) -> bool:
        """
        Helper function for importing a plugin and handling its initialisation.
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
        """
        Loads all configured plugins, as well as the site-local ```plugins.py``, if found.
        """
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
    def register_loader(cls, ext: str, func: Callable[[Path], LoaderResult]):
        """
        Register a file type loader by extension.
        """
        if ext in cls.__loaders__:
            print(f"WARNING: Overriding loader for {ext}")
        cls.__loaders__[ext] = func
        return func

    @classmethod
    def register_context_provider(cls, func: Callable[[dict], dict]):
        """
        Adds a new context provider to the Site.

        Context Providers are applied every time a render needs a template context.
        """
        if func in cls.__context_generators__:
            raise Warning(f"Context generator {func} already registered.")
        cls.__context_generators__.append(func)
        return func

    @emits("render")
    def render(self):
        """
        Loads all content and pages, then renders the site.
        """
        self.load_content()
        self.load_pages()

        self.render_pages()

    @emits("content")
    def load_content(self):
        """
        Builds the 'content' collection for this site, loading all content.
        """
        self.content = Collection(self, loaders=self.__loaders__)
        self.content.load(self.content_dir)
        print(f"Found {len(self.content)} content objects.")

    @emits("pages")
    def load_pages(self):
        """
        Builds the 'pages' collection for this site, loading all content.
        """
        self.pages = Collection(self, default_type=Page, loaders=self.__loaders__)
        self.pages.load(self.pages_dir)
        print(f"Found {len(self.pages)} pages.")

    def render_pages(self):
        """
        Render all pages in this site.
        """
        for name, page in sorted(self.pages.items()):
            print(f"Rendering {name} ...")
            page.render()
        print("-- Done.")

    def get_context(self, obj: Page, **kwargs) -> Context:
        """
        Build a template context object.

        Applies all registered ``context generators``.
        """
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
