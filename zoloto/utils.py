from functools import wraps
from typing import Any, Callable, List, Set, TypeVar

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


def parse_ranges(ranges: str) -> Set[int]:
    """
    Parse a comma seprated list of numbers which may include ranges
    specified as hyphen-separated numbers.
    From https://stackoverflow.com/questions/6405208
    """
    result: List[int] = []
    for part in ranges.split(","):
        if "-" in part:
            a_, b_ = part.split("-")
            a, b = int(a_), int(b_)
            result.extend(range(a, b + 1))
        else:
            a = int(part)
            result.append(a)
    return set(result)
