from collections import defaultdict
from pathlib import Path

from .content import Content
from .query import Query


class Collection:
    """
    Collection of content objects.
    """
    def __init__(self, site, default_type=Content, loaders=None):
        self.site = site
        self.default_type = default_type
        self._items = {}
        self._index = {}
        self._loaders = loaders or {}

    def __getitem__(self, key):
        return self._items[key]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())

    def items(self):
        return self._items.items()

    def matching(self, query):
        """
        Return objects matching a query
        """
        if not isinstance(query, Query):
            query = Query(query)

        return [
            item
            for item in self
            if query(item)
        ]

    def load(self, path: Path, root: Path = None):
        """
        Recursively load all objects from a path.
        """
        if root is None:
            root = path

        for item in path.iterdir():
            if item.is_file():
                name = str(item.relative_to(root))
                self._items[name] = self.load_file(item, name=name)
            elif item.is_dir:
                self.load(item, root)

    def load_file(self, path: Path, name: str):
        ext = path.suffix.lstrip('.')

        load_func = self._loaders.get(ext, load_raw)

        content, meta = load_func(path)

        obj = self.default_type.create(name, self.site, content=content, meta=meta)

        return obj


def load_raw(path: Path):
    '''
    For anything we don't recognise, we load it as a Raw content.
    '''
    return path.read_bytes(), {'content_type': 'Raw'}
