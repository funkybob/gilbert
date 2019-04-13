from pathlib import Path

import yaml

from gilbert import Site


def load_yaml(path: Path):
    with path.open() as fin:
        loader = yaml.Loader(fin)
        data = loader.get_data()
        # PyYAML Reader greedily consumes chunks from the stream.
        # We must recover any un-consumed data, as well as what's left in the stream.
        if loader.buffer:
            content = loader.buffer[loader.pointer:-1]
        else:
            content = ''
        content += fin.read()
    return content, data


Site.register_loader('yaml', load_yaml)
Site.register_loader('yml', load_yaml)
