
class oneshot:
    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        instance.__dict__[self.name] = value = self.func(instance)
        return value
