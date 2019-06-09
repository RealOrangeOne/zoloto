from functools import partial

from zoloto.marker import Marker


def get_uncached_marker_func(marker, func):
    return partial(getattr(marker.__class__, func).func, marker)


def test_marker_distance(benchmark, marker):
    benchmark(get_uncached_marker_func(marker, "distance"))


def test_marker_pixel_corners(benchmark, marker):
    benchmark(lambda: marker.pixel_corners)


def test_marker_pixel_centre(benchmark, marker):
    benchmark(get_uncached_marker_func(marker, "pixel_centre"))


def test_marker_pose_vectors(benchmark, marker):
    benchmark(marker._get_pose_vectors.__wrapped__, marker)


def test_marker_orientation(benchmark, marker):
    benchmark(lambda: marker.orientation)


def test_marker_cartesian(benchmark, marker):
    benchmark(lambda: marker.cartesian)


def test_marker_from_dict(benchmark, marker):
    benchmark(Marker.from_dict, marker.as_dict())
