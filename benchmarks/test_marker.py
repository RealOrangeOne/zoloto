from functools import partial
from typing import Callable

from zoloto.marker import Marker


def get_uncached_marker_func(marker: Marker, func: str) -> partial:
    return partial(getattr(marker.__class__, func).func, marker)


def test_marker_distance(benchmark: Callable, marker: Marker) -> None:
    benchmark(get_uncached_marker_func(marker, "distance"))


def test_marker_pixel_corners(benchmark: Callable, marker: Marker) -> None:
    benchmark(lambda: marker.pixel_corners)


def test_marker_pixel_centre(benchmark: Callable, marker: Marker) -> None:
    benchmark(get_uncached_marker_func(marker, "pixel_centre"))


def test_marker_pose_vectors(benchmark: Callable, marker: Marker) -> None:
    benchmark(marker._get_pose_vectors.__wrapped__, marker)  # type: ignore


def test_marker_orientation(benchmark: Callable, marker: Marker) -> None:
    benchmark(get_uncached_marker_func(marker, "orientation"))


def test_marker_cartesian(benchmark: Callable, marker: Marker) -> None:
    benchmark(lambda: marker.cartesian)


def test_marker_spherical(benchmark: Callable, marker: Marker) -> None:
    benchmark(lambda: marker.spherical)
