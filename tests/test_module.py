from __future__ import annotations

import pytest
from setuptools.config import read_configuration

import zoloto


def test_exposes_version() -> None:
    assert hasattr(zoloto, "__version__")


def test_exposes_marker() -> None:
    assert zoloto.Marker == zoloto.marker.Marker


def test_exposes_marker_type() -> None:
    assert zoloto.MarkerType == zoloto.marker_type.MarkerType


@pytest.mark.parametrize(
    "coordinate_struct",
    ["PixelCoordinates", "Orientation", "CartesianCoordinates", "SphericalCoordinates"],
)
def test_exposes_coordinates(coordinate_struct: str) -> None:
    assert getattr(zoloto, coordinate_struct) == getattr(
        zoloto.coords, coordinate_struct
    )


def test_matching_version() -> None:
    config = read_configuration("setup.cfg")
    assert config["metadata"]["version"] == zoloto.__version__
