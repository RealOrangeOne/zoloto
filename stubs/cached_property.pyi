"""
Type stubs for cached_property.
Note that stubs are only written for the parts that we use.
"""

from typing import Any, Callable, Generic, Optional, Type, TypeVar, overload

_T = TypeVar("_T")
_S = TypeVar("_S")

class cached_property(Generic[_T]):
    func: Callable[[Any], _T]
    attrname: Optional[str]
    def __init__(self, func: Callable[[Any], _T]) -> None: ...
    @overload
    def __get__(
        self, instance: None, owner: Optional[Type[Any]] = ...
    ) -> cached_property[_T]: ...
    @overload
    def __get__(self, instance: _S, owner: Optional[Type[Any]] = ...) -> _T: ...
    def __set_name__(self, owner: Type[Any], name: str) -> None: ...
