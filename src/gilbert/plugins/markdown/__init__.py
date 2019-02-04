from markdown2 import Markdown

from gilbert.collecction import Collection
from gilbert.content import Page


class MarkdownPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        markdown = Markdown()
        self.content = markdown.convert(self.content)


def load_md(path):
    content = path.read_text(encoding='utf-8')

    return {'content_type': 'MarkdownPage'}, content


Collection.register('md', load_md)
