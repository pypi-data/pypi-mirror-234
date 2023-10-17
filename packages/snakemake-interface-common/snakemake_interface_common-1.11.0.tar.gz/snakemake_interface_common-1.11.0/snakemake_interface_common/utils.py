import collections


def not_iterable(value):
    return (
        isinstance(value, str)
        or isinstance(value, dict)
        or not isinstance(value, collections.abc.Iterable)
    )


class lazy_property(property):
    __slots__ = ["method", "cached", "__doc__"]

    @staticmethod
    def clean(instance, method):
        delattr(instance, method)

    def __init__(self, method):
        self.method = method
        self.cached = f"_{method.__name__}"
        super().__init__(method, doc=method.__doc__)

    def __get__(self, instance, owner):
        cached = (
            getattr(instance, self.cached) if hasattr(instance, self.cached) else None
        )
        if cached is not None:
            return cached
        value = self.method(instance)
        setattr(instance, self.cached, value)
        return value
