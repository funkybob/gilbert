from collections import defaultdict
from pathlib import Path

from .content import Content


class Collection:
    """
    Collection of content objects.
    """
    def __init__(self, default_type=Content, loaders=None):
        self.default_type = default_type
        self._items = {}
        self._index = {}
        self._loaders = loaders or {}

    def __getitem__(self, key):
        return self._items[key]

    def items(self):
        return self._items.items()

    def by(self, key):
        """
        Dynamically generate an index by key
        """
        if key not in self._index:
            self._index[key] = CollectionIndex(self, key)
        return self._index[key]

    def with_tag(self, tag):
        """
        Build a set of content with this tag.
        """
        return {
            obj
            for obj in self._items.values()
            if tag in obj.tags
        }

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

        obj = self.default_type.create(name, content=content, meta=meta)

        return obj


def load_raw(path: Path):
    '''
    For anything we don't recognise, we load it as a Raw content.
    '''
    return path.read_bytes(), {'content_type': 'Raw'}


class CollectionIndex(dict):
    def __init__(self, collection: Collection, key: str):
        data = defaultdict(list)
        for obj in collection.values():
            if key in obj:
                data[key].append(obj)
        return super().__init__(data)
