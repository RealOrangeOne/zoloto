"""
Type stubs for fastcache.
Note that stubs are only written for the parts that we use.
"""

from typing import Callable, TypeVar, Optional

T = TypeVar("T")

def clru_cache(maxsize: Optional[int]) -> Callable[..., T]:
    pass
