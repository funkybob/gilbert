import sass

from gilbert import Site
from gilbert.content import Content, Renderable


class SCSS(Renderable, Content):
    output_extension: str = 'css'
    scss_options: dict = {}

    def generate_content(self):
        options = self.scss_options
        if not options:
            options = self.site.config.get('content_type', {}).get('SCSS', {})

        return sass.compile(string=self.content, **options)


def load_scss(path):
    content = path.read_text(encoding='utf-8')

    return content, {'content_type': 'SCSS'}


Site.register_loader('scss', load_scss)
