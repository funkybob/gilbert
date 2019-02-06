import types


class NO_DEFAULT:
    pass


class SchemaProperty:
    def __init__(self, _type, default):
        self._type = _type
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        try:
            return instance.__data__[self.name]
        except KeyError:
            if self.default is NO_DEFAULT:
                raise AttributeError('Schema {} has no value for {}')

        return self.default

    def __set__(self, instance, value):
        if issubclass(self._type, Schema):
            value = self._type(**value)
        else:
            value = self._type(value)
        instance.__data__[self.name] = value


class SchemaType(type):
    def __new__(cls, classname, bases, namespace, **kwargs):
        namespace['__data__'] = {}

        for name, _type in namespace.get('__annotations__', {}).items():
            if name.startswith('__') and name.endswith('__'):
                continue

            default = namespace.get(name, NO_DEFAULT)

            if isinstance(default, types.FunctionType):
                continue

            namespace[name] = SchemaProperty(_type, default)

        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Schema(object, metaclass=SchemaType):
    __slots__ = ()

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
