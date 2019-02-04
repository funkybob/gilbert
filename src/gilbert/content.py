"""
Content object classes
"""


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

    def __getitem__(self, key, default=None):
        """
        Provide dict-alike access to our data.
        """
        return self.data.get(key, default)

    def render(self, site):
        """
        """


class Page(Content):

    def get_template_names(self):
        return [
            self.data.get('template', 'default.html'),
        ]

    def get_template(self, site):
        template_names = self.get_template_names()
        for name in template_names:
            try:
                template = site.templates[self.data['template']]
                break
            except KeyError:
                pass
        else:
            raise ValueError(f'Template for {name} not found: {template_names}')

        return template

    def get_context(self, site):
        return site.get_context(self)

    def get_output_name(self, site):
        return Path(self.name).with_suffix('.html')

    def render(self, site):
        template = self.get_template(site)
        context = self.get_context(site)

        with (site.dest_dir / self.get_output_name()).open('w') as fout:
            template.render(context, output=fout)
