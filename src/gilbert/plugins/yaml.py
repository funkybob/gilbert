"""
Provides a general YAML file loader.
"""

from pathlib import Path

import yaml

from gilbert.site import Site
from gilbert.types import LoaderResult


def load_yaml(path: Path) -> LoaderResult:
    """
    Loads a YAML file.

    Reads the first "document" (up to the '---' line) as meta, and treats the remainder of the file as content.
    """
    with path.open() as fin:
        loader = yaml.Loader(fin)
        meta = loader.get_data()
        # PyYAML Reader greedily consumes chunks from the stream.
        # We must recover any un-consumed data, as well as what's left in the stream.
        if loader.buffer:
            data = loader.buffer[loader.pointer : -1]
        else:
            data = ""
        data += fin.read()
    return data, meta


Site.register_loader("yaml", load_yaml)
Site.register_loader("yml", load_yaml)
