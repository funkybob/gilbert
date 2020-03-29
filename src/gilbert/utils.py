from functools import update_wrapper


class oneshot:
    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        instance.__dict__[self.name] = value = self.func(instance)
        return value
