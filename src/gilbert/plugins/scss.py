from scss import Compiler

from gilbert import Site
from gilbert.content import Content, Renderable


class SCSS(Renderable, Content):
    output_extension: str = 'css'
    scss_options: dict = {}

    def generate_content(self):
        compiler = Compiler(**self.scss_options)

        return compiler.compile_string(self.content)


def load_scss(path):
    content = path.read_text(encoding='utf-8')

    return content, {'content_type': 'SCSS'}


Site.register_loader('scss', load_scss)
Site.register_loader('css', load_scss)
