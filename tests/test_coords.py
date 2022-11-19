"""Tests for coordinates classes."""
from __future__ import annotations

from hypothesis import given
from hypothesis.strategies import floats, tuples
from pyquaternion import Quaternion

from zoloto.coords import Orientation


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
