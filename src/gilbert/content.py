"""
Content object classes
"""
from pathlib import Path


class Content:
    _types = {}

    def __init__(self, name, data=None, content=None):
        self.name = name
        self.data = data or {}
        self.content = content or ''

    def __init_subclass__(cls, **kwargs):
        """
        Catch-subclass declarations and register them.
        """
        super().__init_subclass__(**kwargs)
        cls._types[cls.__name__] = cls

    @classmethod
    def create(cls, name, data, *args, **kwargs):
        content_type = data.get('content_type', cls.__name__)
        klass = cls._types[content_type]
        return klass(name, data, *args, **kwargs)


class Raw(Content):
    """
    Container for 'raw' content.
    """
    def render(self, site):
        (site.dest_dir / self.name).write_bytes(self.content)


class Page(Content):

    def get_template_names(self):
        template = self.data.get('template', [])
        if isinstance(template, str):
            template = [template]

        return template + ['default.html']

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

    def get_output_name(self):
        target_ext = self.data.get('extension', 'html')
        return Path(self.name).with_suffix(f'.{target_ext}')

    def render(self, site):
        template = self.get_template(site)
        context = self.get_context(site)

        with (site.dest_dir / self.get_output_name()).open('w') as fout:
            template.render(context, output=fout)
