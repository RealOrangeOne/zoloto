import pytest

import zoloto


def test_exposes_version():
    assert hasattr(zoloto, "__version__")


def test_exposes_marker():
    assert zoloto.Marker == zoloto.marker.Marker


def test_exposes_marker_dict():
    assert zoloto.MarkerDict == zoloto.marker_dict.MarkerDict


@pytest.mark.parametrize(
    "coordinate_struct",
    ["Coordinates", "Orientation", "ThreeDCoordinates", "Spherical"],
)
def test_exposes_coordinates(coordinate_struct):
    assert getattr(zoloto, coordinate_struct) == getattr(
        zoloto.coords, coordinate_struct
    )
