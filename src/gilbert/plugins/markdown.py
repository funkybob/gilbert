from markdown2 import Markdown

from gilbert import Site
from gilbert.content import Content, Templated
from gilbert.utils import oneshot


class MarkdownPage(Templated, Content):
    extras: list = []

    @oneshot
    def content(self):
        extras = self.extras
        if not extras:
            extras = self.site.config.get('content_type', {}).get('MarkdownPage', [])

        self._markdown = Markdown(extras=extras)
        return self._markdown.convert(self.data)


def load_md(path):
    data = path.read_text(encoding='utf-8')

    return data, {'content_type': 'MarkdownPage'}


Site.register_loader('md', load_md)
