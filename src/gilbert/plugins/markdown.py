from markdown2 import Markdown

from gilbert import Site
from gilbert.content import Content, Templated


class MarkdownPage(Templated, Content):
    extras: list = []

    def __init__(self, name, site, content=None, meta=None):
        super().__init__(name, site, content=content, meta=meta)
        markdown = Markdown(extras=self.extras)
        self.raw_content = self.content
        self.content = markdown.convert(content)


def load_md(path):
    content = path.read_text(encoding='utf-8')

    return content, {'content_type': 'MarkdownPage'}


Site.register_loader('md', load_md)
