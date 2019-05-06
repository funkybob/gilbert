

class Query:
    def __init__(self, expr):
        self.query = AstNode.build(expr)

    def __call__(self, context):
        return self.query(context)


class AstNode:
    __ops__ = {}

    def __init_subclass__(cls, operator, **kwargs):
        super().__init_subclass__(**kwargs)
        if operator is not None:
            AstNode.__ops__[operator] = cls

    @staticmethod
    def build(term):
        if isinstance(term, (int, float, str)):
            return term

        operator, args = term.popitem()
        assert not len(term)

        args = [AstNode.build(arg) for arg in args]
        try:
            return AstNode.__ops__[operator](*args)
        except TypeError:
            print(operator, args)
            raise

    def resolve(self, term, context):
        if isinstance(term, (int, float, str)):
            return term

        return term(context)


class Attr(AstNode, operator='attr'):
    def __init__(self, name):
        self.name = name

    def __call__(self, context):
        name = self.resolve(self.name, context)

        return getattr(context, name)


class StartsWith(AstNode, operator='startswith'):
    def __init__(self, value, prefix):
        self.value = value
        self.prefix = prefix

    def __call__(self, context):
        value = self.resolve(self.value, context)
        prefix = self.resolve(self.prefix, context)

        return value.startswith(prefix)
