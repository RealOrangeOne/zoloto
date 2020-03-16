import json
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar("T", bound=Callable)


def cached_method(f: T) -> T:
    """
    Caches the return value for a class instance method.
    The cache is tied to the instance, rather than the class
    """

    @wraps(f)
    def wrapper(obj: Any, *args: Any, **kwargs: Any) -> None:
        value = f(obj, *args, **kwargs)
        obj.__dict__[f.__name__] = lambda *args, **kwargs: value
        return value

    wrapper.__wrapped__ = f  # type: ignore
    return wrapper  # type: ignore


def encode_as_json(o: Any) -> str:
    try:
        import ujson

        return ujson.dumps(o)
    except ImportError:
        return json.dumps(o)