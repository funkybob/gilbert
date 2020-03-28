from markdown import markdown

from gilbert import Site
from gilbert.content import Page
from gilbert.utils import oneshot


class MarkdownPage(Page):
    extras: list = []

    @oneshot
    def content(self):
        extras = self.extras
        if not extras:
            extras = self.site.config.get("content_type", {}).get("MarkdownPage", [])

        return markdown(self.data, output_format="html5", extensions=extras)


def load_md(path):
    data = path.read_text(encoding="utf-8")

    return data, {"content_type": "MarkdownPage"}


Site.register_loader("md", load_md)
