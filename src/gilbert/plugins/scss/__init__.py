from scss import Compiler

from gilbert.content import ContentObject


class SCSS(DataObject):

    def get_output_name(self, site):
        return Path(self.name).with_suffix('.css')

    def render(self, site):
        compiler_args = self.data.get('scss_options', {})
        compiler = Compiler(**compiler_args)

        with (site.dest_dir / self.get_output_name()).open('w') as fout:
            fout.write(compiler.compile_string(self.content))
