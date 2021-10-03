from typing import Iterator, NamedTuple, Tuple

from cached_property import cached_property
from cv2 import Rodrigues
from pyquaternion import Quaternion


class Coordinates(NamedTuple):
    """
    :param float x: X coordinate
    :param float y: Y coordinate
    """

    x: float
    y: float


class ThreeDCoordinates(NamedTuple):
    """
    :param float x: X coordinate
    :param float y: Y coordinate
    :param float z: Z coordinate
    """

    x: float
    y: float
    z: float


class Spherical(NamedTuple):
    """
    :param float rot_x: Rotation around the X-axis, in radians
    :param float rot_y: Rotation around the Y-axis, in radians
    :param float dist: Distance
    """

    rot_x: float
    rot_y: float
    dist: int


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
        """Get rotation angle around x axis in radians."""
        return self.roll

    @property
    def rot_y(self) -> float:
        """Get rotation angle around y axis in radians."""
        return self.pitch

    @property
    def rot_z(self) -> float:
        """Get rotation angle around z axis in radians."""
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
        return "Orientation(rot_x={},rot_y={},rot_z={})".format(
            self.rot_x, self.rot_y, self.rot_z
        )
