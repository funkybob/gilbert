from markdown2 import Markdown

from gilbert.collection import Collection
from gilbert.content import Content, Renderable


class MarkdownPage(Renderable, Content):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_content(self, site, target):
        markdown = Markdown()
        target.write(markdown.convert(self.content))


def load_md(path):
    content = path.read_text(encoding='utf-8')

    return content, {'content_type': 'MarkdownPage'}


Collection.register('md', load_md)
