from pathlib import Path

from markdown import markdown

from gilbert import Site
from gilbert.content import Page
from gilbert.types import LoaderResult
from gilbert.utils import oneshot


class MarkdownPage(Page):
    extras: list = []

    @oneshot
    def content(self) -> str:
        extras = self.extras
        if not extras:
            extras = self.site.config.get("content_type", {}).get("MarkdownPage", [])

        return markdown(self.data, output_format="html5", extensions=extras)


def load_md(path: Path) -> LoaderResult:
    data = path.read_text(encoding="utf-8")

    return data, {"content_type": "MarkdownPage"}


Site.register_loader("md", load_md)
