from markdown2 import Markdown

from gilbert.content import Page


class MarkdownPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        markdown = Markdown()
        self.content = markdown.convert(self.content)
