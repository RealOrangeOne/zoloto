"""Tests for coordinates classes."""
from __future__ import annotations

import math

import pytest
from hypothesis import given
from hypothesis.strategies import floats, tuples
from pyquaternion import Quaternion

from zoloto.coords import CartesianCoordinates, Orientation, SphericalCoordinates


@given(tuples(floats(), floats(), floats()))
def test_valid_conversion(euler_angles: tuple[float, float, float]) -> None:
    """
    Test conversion from the vector.

    Tests that yaw, pitch, roll, etc. are equal.
    """
    q = Quaternion(axis=euler_angles, scalar=1)
    orientation = Orientation(*q.vector)

    assert q.yaw_pitch_roll == orientation.yaw_pitch_roll
    assert tuple(map(tuple, q.rotation_matrix)) == orientation.rotation_matrix
    assert q == orientation.quaternion


@given(tuples(floats(), floats(), floats()))
def test_rot_yaw_pitch_roll(euler_angles: tuple[float, float, float]) -> None:
    """Test that x,y,z are equal to yaw, pitch, roll."""
    q = Quaternion(axis=euler_angles, scalar=1)
    orientation = Orientation(*q.vector)

    assert orientation.rot_x == orientation.roll
    assert orientation.rot_y == orientation.pitch
    assert orientation.rot_z == orientation.yaw


@given(tuples(floats(), floats(), floats()))
def test_iterator(euler_angles: tuple[float, float, float]) -> None:
    """Test that the iterator returns the correct values."""
    q = Quaternion(axis=euler_angles, scalar=1)
    orientation = Orientation(*q.vector)

    ypr = q.yaw_pitch_roll

    assert list(orientation) == [
        ypr[2],
        ypr[1],
        ypr[0],
    ]


@given(tuples(floats(), floats(), floats()))
def test_repr(euler_angles: tuple[float, float, float]) -> None:
    """Test that the representation is as expected."""
    q = Quaternion(axis=euler_angles, scalar=1)
    orientation = Orientation(*q.vector)

    ypr = q.yaw_pitch_roll
    names = ["rot_z", "rot_y", "rot_x"]

    repr_str = repr(orientation)

    for name, val in zip(names, ypr):
        assert f"{name}={val}" in repr_str


@pytest.mark.parametrize(
    "cartesian,expected",
    [
        pytest.param(
            CartesianCoordinates(0, 0, 0),
            SphericalCoordinates(0, 0, 0),
            id="origin",
        ),
        pytest.param(
            CartesianCoordinates(0, 0, 1),
            SphericalCoordinates(
                theta=math.pi / 2,
                phi=math.pi / 2,
                distance=1,
            ),
            id="in-front-of-you",
        ),
        pytest.param(
            CartesianCoordinates(0, 1, 0),
            SphericalCoordinates(
                theta=0,
                phi=0,
                distance=1,
            ),
            id="above-you",
        ),
        pytest.param(
            CartesianCoordinates(1, 0, 0),
            SphericalCoordinates(
                theta=math.pi / 2,
                phi=0,
                distance=1,
            ),
            id="to-one-side",
        ),
        pytest.param(
            CartesianCoordinates(1000, 1000, 0),
            SphericalCoordinates(
                theta=0.7853981633974484,  # math.pi / 4, with floating point error
                phi=0,
                distance=1414,
            ),
            id="to-one-side-and-up",
        ),
    ],
)
def test_spherical_from_cartesian(
    cartesian: CartesianCoordinates,
    expected: SphericalCoordinates,
) -> None:
    spherical = SphericalCoordinates.from_cartesian(cartesian)
    assert spherical == expected
