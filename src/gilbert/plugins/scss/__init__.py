from pathlib import Path

from scss import Compiler

from gilbert.content import Content
from gilbert.collection import Collection


class SCSS(Content):

    scss_options: dict = {}

    def get_output_name(self):
        return Path(self.name).with_suffix('.css')

    def render(self, site):
        compiler = Compiler(**self.scss_options)

        with (site.dest_dir / self.get_output_name()).open('w') as fout:
            fout.write(compiler.compile_string(self.content))


def load_scss(path):
    content = path.read_text(encoding='utf-8')

    return content, {'content_type': 'SCSS'}


Collection.register('scss', load_scss)
