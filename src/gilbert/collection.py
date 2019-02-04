from collections import defaultdict
from pathlib import Path

import yaml

from .content import Content


class Collection:
    """
    Collection of content objects.
    """

    def __init__(self, default_type=Content):
        self.default_type = default_type
        self._items = {}
        self._index = {}

    def items(self):
        return self._items.items()

    def by(self, key):
        """
        Dynamically generate an index by key
        """
        if key not in self._index:
            self._index[key] = CollectionIndex(self, key)
        return self._index[key]

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

        load_func = getattr(self, f'load_file_{ext}', self.load_file_yaml)
        args = load_func(path)

        obj = self.default_type.create(name, *args)

        return obj

    def load_file_yaml(self, path: Path):
        with path.open() as fin:
            loader = yaml.Loader(fin)
            data = loader.get_data()
            # PyYAML Reader greedily consumes chunks from the stream.
            # We must recover any un-consumed data, as well as what's left in the stream.
            if loader.buffer:
                content = loader.buffer[loader.pointer:]
            else:
                content = ''
            content += fin.read()
        return data, content

    load_file_yml = load_file_yaml

    def load_file_scss(self, path: Path):
        content = path.read_text(encoding='utf-8')

        return {'content_type': 'SCSS'}, content

    def load_file_md(self, path: Path):
        content = path.read_text(encoding='utf-8')

        return {'content_type': 'MarkdownPage'}, contente


class CollectionIndex(dict):
    def __init__(self, collection: Collection, key: str):
        data = defaultdict(list)
        for obj in collection.values():
            if key in obj:
                data[key].append(obj)
        return super().__init__(data)
