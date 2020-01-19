"""
Type stubs for cached_property.
Note that stubs are only written for the parts that we use.
"""

from typing import Callable, Type, TypeVar

T = TypeVar("T")
U = TypeVar("U")

class cached_property(object):
    def __init__(self, func: Callable[..., T]) -> None: ...
    def __get__(self, obj: U, cls: Type[U]) -> T: ...
