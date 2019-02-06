"""
Content object classes
"""
from pathlib import Path
from typing import Union, Sequence

from .schema import Schema


class Content(Schema):
    _types = {}

    content_type: str

    content: str

    def __init__(self, name, content=None, meta=None):
        self.name = name
        self.content = content or ''
        super().__init__(**meta)

    def __init_subclass__(cls, **kwargs):
        """
        Catch-subclass declarations and register them.
        """
        super().__init_subclass__(**kwargs)
        cls._types[cls.__name__] = cls

    @classmethod
    def create(cls, name, content, meta):
        content_type = meta.get('content_type', cls.__name__)
        klass = cls._types[content_type]
        return klass(name, content, meta)


class Raw(Content):
    """
    Container for 'raw' content.
    """
    def render(self, site):
        (site.dest_dir / self.name).write_bytes(self.content)


class Renderable:
    """
    Mixin to simplify making renderable content types.
    """
    extension: str = 'html'

    def get_output_name(self):
        return Path(self.name).with_suffix(f'.{self.extension}')

    def generate_content(self, site, target):
        target.write(self.content)

    def render(self, site):
        with (site.dest_dir / self.get_output_name()).open('w') as fout:
            self.generate_content(site, fout)


class Templated(Renderable):
    """
    Definition and implementation of the Templated interface.
    """
    template: Union[str, Sequence[str]] = 'default.html'

    def get_template_names(self):
        template = self.template
        if isinstance(template, str):
            template = [template]

        return template

    def get_template(self, site):
        template_names = self.get_template_names()
        for name in template_names:
            try:
                template = site.templates[name]
                break
            except LookupError:
                pass
        else:
            raise ValueError(f'Template for {name} not found: {template_names}')

        return template

    def get_context(self, site):
        return site.get_context(self)

    def generate_content(self, site, target):
        template = self.get_template(site)
        context = self.get_context(site)

        template.render(context, output=target)


class Page(Templated, Content):
    pass
