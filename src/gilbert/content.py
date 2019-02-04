"""
Content object classes
"""


class ContentObject:
    _types = {}

    def __init__(self, name):
        self.name = name

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

    def render(self, context):
        """
        """


class DataObject(ContentObject):
    """
    A simple, generic Data container object.
    """
    def __init__(self, name, data):
        super().__init__(name)
        self.data = data

    def __getitem__(self, key, default=None):
        return self.data.get(key, default)


class Page(ContentObject):

    def __init__(self, name, data, content=None):
        super().__init__(name)
        self.data = data
        self.content = content or ''

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
            template=  site.templates['default.html']

        return template

    def get_context(self, site):
        return site.get_context(self)

    def render(self, site):
        template = self.get_template(site)
        context = self.get_context(site)

        with (site.dest_dir / self.name).with_suffix('.html').open('w') as fout:
            template.render(context, output=fout)
