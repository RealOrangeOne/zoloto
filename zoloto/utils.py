import json
from functools import wraps
from typing import Any, Callable, TypeVar

try:
    import ujson
except ImportError:  # pragma: nocover
    ujson = None  # type: ignore


T = TypeVar("T", bound=Callable[[Any], Any])


def cached_method(f: T) -> T:
    """
    Caches the return value for a class instance method.
    The cache is tied to the instance, rather than the class
    """

    @wraps(f)
    def wrapper(obj: Any) -> Any:
        value = f(obj)
        obj.__dict__[f.__name__] = lambda: value
        return value

    wrapper.__wrapped__ = f  # type: ignore
    return wrapper  # type: ignore


def encode_as_json(data: Any) -> str:
    """
    Wrapper for json conversion which uses `ujson` if available.
    """
    if ujson is not None:
        return ujson.dumps(data)
    return json.dumps(data)
