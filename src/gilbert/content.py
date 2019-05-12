"""
Content object classes
"""
from pathlib import Path
from typing import Collection, Sequence, Union

from .exceptions import ClientException
from .schema import Schema
from .utils import oneshot


class Content(Schema):
    """
    Base content class.
    """
    _types = {}

    content_type: str

    content: str
    tags: Collection[str] = []

    def __init__(self, name, site, content=None, meta=None):
        self.name = name
        self.site = site
        self.content = content or ''
        super().__init__(**meta)

    def __init_subclass__(cls, **kwargs):
        """
        Catch-subclass declarations and register them.
        """
        super().__init_subclass__(**kwargs)
        cls._types[cls.__name__] = cls

    @classmethod
    def create(cls, name, site, content, meta):
        """
        Create a new Content instance.

        Will extract the content type from the meta, and create the
        appropriate sub-class.
        """
        content_type = meta.get('content_type', cls.__name__)
        try:
            klass = cls._types[content_type]
        except KeyError:
            raise ValueError(
                f'You attempted to create a page with type "{content_type}" but no class is registered to handle this'
                ' content type'
            )
        return klass(name, site, content=content, meta=meta)


class Raw(Content):
    """
    Container for 'raw' content.
    """
    content: bytes

    def render(self):
        target = self.site.dest_dir / self.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.content)


class Renderable:
    """
    Mixin to simplify making renderable content types.
    """
    output_extension: str = 'html'

    @oneshot
    def output_filename(self):
        return Path(self.name).with_suffix(f'.{self.output_extension}')

    @oneshot
    def url(self):
        return f'/{self.output_filename}'

    def generate_content(self):
        return self.content

    def render(self):
        target = self.site.dest_dir / self.output_filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            self.generate_content()
        )


class Templated(Renderable):
    """
    Definition and implementation of the Templated interface.
    """
    template: Union[str, Sequence[str]] = 'default.html'

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
            raise ClientException(f'Template for {name} not found: {template_names}')

        return template

    def get_context(self):
        return self.site.get_context(self)

    def generate_content(self):
        template = self.get_template()
        context = self.get_context()

        try:
            return template.render(context)
        except Exception as ex:
            raise ClientException(f'Error rendering template "{template.name}": {ex.args[0]}')


class Page(Templated, Content):
    """
    A templated Page content type.
    """
