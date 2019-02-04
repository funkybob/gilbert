from pathlib import Path

from scss import Compiler

from gilbert.content import Content
from gilbert.collection import Collection


class SCSS(Content):

    def get_output_name(self):
        return Path(self.name).with_suffix('.css')

    def render(self, site):
        compiler_args = self.data.get('scss_options', {})
        compiler = Compiler(**compiler_args)

        with (site.dest_dir / self.get_output_name()).open('w') as fout:
            fout.write(compiler.compile_string(self.content))


def load_scss(path):
    content = path.read_text(encoding='utf-8')

    return {'content_type': 'SCSS'}, content


Collection.register('scss', load_scss)
