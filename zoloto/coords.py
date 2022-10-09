from __future__ import annotations

import math
from typing import Iterator, NamedTuple, Tuple

from cached_property import cached_property
from cv2 import Rodrigues
from pyquaternion import Quaternion


class PixelCoordinates(NamedTuple):
    """
    Coordinates within an image made up from pixels.

    This type allows float values to account for computed locations which are
    not limited to exact pixel boundaries.

    :param float x: X coordinate
    :param float y: Y coordinate
    """

    x: float
    y: float


class CartesianCoordinates(NamedTuple):
    """
    Cartesian coordinates, rotated on their side.

    The X axis is horizontal relative to the camera's perspective, i.e: left &
    right within the frame of the image. Zero is at the centre of the image.
    Increasing values indicate greater distance to the right.

    The Y axis is vertical relative to the camera's perspective, i.e: up & down
    within the frame of the image. Zero is at the centre of the image.
    Increasing values indicate greater distance below the centre of the image.

    The Z axis extends directly away from the camera. Zero is at the camera.
    Increasing values indicate greater distance from the camera.

    These match traditional cartesian coordinates when the camera is facing
    upwards.

    :param float x: X coordinate
    :param float y: Y coordinate
    :param float z: Z coordinate
    """

    x: float
    y: float
    z: float


class SphericalCoordinates(NamedTuple):
    """
    SphericalCoordinates coordinates, rotated onto their side.

    This is comparable to the ISO convention for spherical coordinates, applied
    to our rotated axes. Here θ is measured down from the y-axis (rather than
    the usual z-axis) while φ is measured around the y-axis.

    See https://en.wikipedia.org/wiki/Spherical_coordinate_system and
    https://studentrobotics.org/docs/programming/sr/vision/#SphericalCoordinates.

    :param float distance: Radial distance from the origin.
    :param float theta: Polar angle, θ, in radians. This is the angle "down"
        from the y-axis to the vector which points to the location. For points
        with zero cartesian x-coordinate value, this can be viewed as the
        rotation about the x-axis. Zero is on the positive y-axis.
    :param float phi: Azimuth angle, φ, in radians. This is the angle from the
        x-axis around the polar (y-axis) to the projection of the point on the
        x-z plane. This can be viewed as rotation about the y-axis. Zero is at
        the centre of the image.
    """

    distance: int
    theta: float
    phi: float

    @property
    def rot_x(self) -> float:
        return self.theta

    @property
    def rot_y(self) -> float:
        return self.phi

    @classmethod
    def from_cartesian(cls, cartesian: CartesianCoordinates) -> SphericalCoordinates:
        if not any(cartesian):
            return SphericalCoordinates(0, 0, 0)

        distance = math.sqrt(sum(x**2 for x in cartesian))
        x, y, z = cartesian
        return SphericalCoordinates(
            distance=int(distance),
            theta=math.acos(y / distance),
            phi=math.atan2(z, x),
        )


ThreeTuple = Tuple[float, float, float]
RotationMatrix = Tuple[ThreeTuple, ThreeTuple, ThreeTuple]


class Orientation:
    """The orientation of an object in 3-D space."""

    def __init__(self, e_x: float, e_y: float, e_z: float):
        """
        Construct a quaternion given the components of a rotation vector.

        More information: https://w.wiki/Fci
        """
        rotation_matrix, _ = Rodrigues((e_x, e_y, e_z))
        self._quaternion = Quaternion(matrix=rotation_matrix)

    @property
    def rot_x(self) -> float:
        """
        Get rotation angle around X axis in radians.

        The X axis is horizontal relative to the camera's perspective, i.e: left
        & right within the frame of the image.

        Increasing values represent an increasing clockwise rotation of the
        marker as seen from the camera's left.

        Zero values for April Tags markers have the marker facing away from the
        camera. The practical effect of this is that an April Tags marker facing
        the camera square-on will have a value of ``pi`` (or equivalently
        ``-pi``) and the value will decrease as the marker diverges from
        square-on.

        For observed markers positive values therefore indicate a rotation of
        the top of the marker away from the camera, such that marker could be
        said to be leaning backwards, with the value decreasing as the marker
        leans back further.
        """
        return self.roll

    @property
    def rot_y(self) -> float:
        """
        Get rotation angle around Y axis in radians.

        The Y axis is vertical relative to the camera's perspective, i.e: up &
        down within the frame of the image.

        Positive values indicate a rotation of an observed marker towards the
        camera's right. This is a rotation of the marker counter-clockwise about
        the Y axis as seen from above the marker.

        Zero values for April Tags markers have the marker facing the camera
        square-on.
        """
        return self.pitch

    @property
    def rot_z(self) -> float:
        """
        Get rotation angle around Z axis in radians.

        The Z axis extends directly away from the camera.

        Positive values indicate a rotation counter-clockwise from the
        perspective of the camera.

        Zero values for April Tags markers have the marker reference point at
        the top left.
        """
        return self.yaw

    @property
    def yaw(self) -> float:
        """Get rotation angle around z axis in radians."""
        return self.yaw_pitch_roll[0]

    @property
    def pitch(self) -> float:
        """Get rotation angle around y axis in radians."""
        return self.yaw_pitch_roll[1]

    @property
    def roll(self) -> float:
        """Get rotation angle around x axis in radians."""
        return self.yaw_pitch_roll[2]

    @cached_property
    def yaw_pitch_roll(self) -> ThreeTuple:
        """
        Get the equivalent yaw-pitch-roll angles.

        Specifically intrinsic Tait-Bryan angles following the z-y'-x'' convention.
        """
        return self._quaternion.yaw_pitch_roll

    def __iter__(self) -> Iterator[float]:
        """
        Get an iterator over the rotation angles.

        Returns:
            An iterator of floating point angles in order x, y, z.
        """
        return iter([self.rot_x, self.rot_y, self.rot_z])

    @cached_property
    def rotation_matrix(self) -> RotationMatrix:
        """
        Get the rotation matrix represented by this orientation.

        Returns:
            A 3x3 rotation matrix as a tuple of tuples.
        """
        r_m = self._quaternion.rotation_matrix
        return (
            (r_m[0][0], r_m[0][1], r_m[0][2]),
            (r_m[1][0], r_m[1][1], r_m[1][2]),
            (r_m[2][0], r_m[2][1], r_m[2][2]),
        )

    @property
    def quaternion(self) -> Quaternion:
        """Get the quaternion represented by this orientation."""
        return self._quaternion

    def __repr__(self) -> str:
        return "Orientation(rot_x={}, rot_y={}, rot_z={})".format(
            self.rot_x, self.rot_y, self.rot_z
        )
