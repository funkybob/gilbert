"""
Content object classes
"""
from pathlib import Path
from shutil import copyfileobj
from typing import Collection, Dict, Sequence, Union

from .exceptions import ClientException
from .schema import Schema
from .utils import oneshot


class Content(Schema):
    """
    Base content class.
    """

    __registry__: Dict[str, Schema] = {}

    content_type: str

    tags: Collection[str] = []

    def __init__(self, name, site, data=None, meta=None):
        self.name = name
        self.site = site
        self.data = data or ""
        meta = meta or {}
        super().__init__(**meta)

    def __init_subclass__(cls, **kwargs):
        """
        Catch-subclass declarations and register them.
        """
        super().__init_subclass__(**kwargs)
        cls.__registry__[cls.__name__] = cls

    @classmethod
    def create(cls, name, site, data, meta):
        """
        Create a new Content instance.

        Will extract the content type from the meta, and create the
        appropriate sub-class.
        """
        content_type = meta.get("content_type", cls.__name__)
        try:
            klass = cls.__registry__[content_type]
        except KeyError:
            raise ValueError(
                f'You attempted to create a page with type "{content_type}" but no class is registered to handle this'
                " content type"
            )
        return klass(name, site, data=data, meta=meta)

    @property
    def content(self):
        return self.data


class Raw(Content):
    """
    Container for 'raw' data.

    Unlike other content types, does not hold its data - only the path to the source.
    Upon render, it copies the source file directly to the target.
    """

    path: Path

    def render(self):
        target = self.site.dest_dir / self.name
        target.parent.mkdir(parents=True, exist_ok=True)
        copyfileobj(self.path.open("rb"), target.open("wb"))


class Renderable:
    """
    Mixin to simplify making renderable content types.
    """

    name: str
    output_extension: str = "html"

    @oneshot
    def output_filename(self) -> Path:
        return Path(self.name).with_suffix(f".{self.output_extension}")

    @oneshot
    def url(self) -> str:
        return f"/{self.output_filename}"

    @oneshot
    def page_content(self):
        return self.content

    def render(self):
        target = self.site.dest_dir / self.output_filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.content)


class Templated(Renderable):
    """
    Definition and implementation of the Templated interface.
    """

    template: Union[str, Sequence[str]] = "default.html"

    def get_template_names(self) -> Sequence[str]:
        template = self.template
        if isinstance(template, str):
            template = [template]

        return template

    def get_template(self):
        template_names = self.get_template_names()
        for name in template_names:
            try:
                template = self.site.templates[name]
                break
            except LookupError:
                pass
        else:
            raise ClientException(f"Template for {name} not found: {template_names}")

        return template

    def get_context(self):
        return self.site.get_context(self)

    @oneshot
    def page_content(self):
        template = self.get_template()
        context = self.get_context()

        try:
            return template.render(context)
        except Exception as ex:
            raise ClientException(f'Error rendering template "{template.name}": {ex.args[0]}')

    def render(self):
        target = self.site.dest_dir / self.output_filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.page_content)


class Page(Templated, Content):
    """
    A templated Page content type.
    """
