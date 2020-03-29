from pathlib import Path

import sass

from gilbert import Site
from gilbert.content import Content, Renderable
from gilbert.types import LoaderResult
from gilbert.utils import oneshot


class SCSS(Renderable, Content):
    """
    Content type that renders its content as SCSS

    Additional options can be configured globally in ``config.yml``:

    content_type:SCSS:

    or using the ``scss_options`` attribute.
    """

    output_extension: str = "css"
    scss_options: dict = {}

    @oneshot
    def content(self):
        options = self.scss_options
        if not options:
            options = self.site.config.get("content_type", {}).get("SCSS", {})

        return sass.compile(string=self.data, **options)


def load_scss(path: Path) -> LoaderResult:
    data = path.read_text(encoding="utf-8")

    return data, {"content_type": "SCSS"}


Site.register_loader("scss", load_scss)
