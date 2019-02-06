from pathlib import Path

from scss import Compiler

from gilbert.content import Content, Renderable
from gilbert.collection import Collection


class SCSS(Renderable, Content):

    scss_options: dict = {}

    def get_output_name(self):
        return Path(self.name).with_suffix('.css')

    def generate_content(self, site, target):
        compiler = Compiler(**self.scss_options)

        target.write(compiler.compile_string(self.content))


def load_scss(path):
    content = path.read_text(encoding='utf-8')

    return content, {'content_type': 'SCSS'}


Collection.register('scss', load_scss)
