from pathlib import Path

from scss import Compiler

from gilbert.content import Content, Renderable
from gilbert.collection import Collection


class SCSS(Renderable, Content):
    output_extension: str = 'css'
    scss_options: dict = {}

    def generate_content(self, site):
        compiler = Compiler(**self.scss_options)

        return compiler.compile_string(self.content)


def load_scss(path):
    content = path.read_text(encoding='utf-8')

    return content, {'content_type': 'SCSS'}


Collection.register('scss', load_scss)
