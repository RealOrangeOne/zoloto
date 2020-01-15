from typing import Iterator, NamedTuple, Tuple

from cached_property import cached_property
from coordinates import spaced_coordinate
from cv2 import Rodrigues
from numpy import ndarray
from pyquaternion import Quaternion

Coordinates = spaced_coordinate("Coordinates", "xy")

ThreeDCoordinates = spaced_coordinate("ThreeDCoordinates", "xyz")

Spherical = NamedTuple("Spherical", [("rot_x", float), ("rot_y", float), ("dist", int)])


class Orientation:
    """The orientation of an object in 3-D space."""

    def __init__(self, *rvec) -> None:
        rotation_matrix, _ = Rodrigues(rvec)
        self._quaternion = Quaternion(matrix=rotation_matrix)

    @property
    def rot_x(self) -> float:
        """Get rot_x aka. roll."""
        return self.roll

    @property
    def rot_y(self) -> float:
        """Get rot_y aka. pitch."""
        return self.pitch

    @property
    def rot_z(self) -> float:
        """Get rot_z aka. yaw."""
        return self.yaw

    @property
    def yaw(self) -> float:
        """The yaw of the rotation."""
        return self.yaw_pitch_roll[0]

    @property
    def pitch(self) -> float:
        """The pitch of the rotation."""
        return self.yaw_pitch_roll[1]

    @property
    def roll(self) -> float:
        """The roll of the rotation."""
        return self.yaw_pitch_roll[2]

    @cached_property
    def yaw_pitch_roll(self) -> Tuple[float, float, float]:
        """
        Get the equivalent yaw-pitch-roll angles.

        Specifically intrinsic Tait-Bryan angles following the z-y'-x'' convention.

        Returns:
            A three-tuple of floating point angles:
            yaw:    rotation angle around the z-axis in radians, in the range `[-pi, pi]`
            pitch:  rotation angle around the y'-axis in radians, in the range `[-pi/2, -pi/2]`
            roll:   rotation angle around the x''-axis in radians, in the range `[-pi, pi]`
        """
        return self._quaternion.yaw_pitch_roll

    def __iter__(self) -> Iterator[float]:
        return iter([self.rot_x, self.rot_y, self.rot_z])

    @cached_property
    def rotation_matrix(self) -> ndarray:
        """Get the rotation matrix represented by this orientation."""
        return self._quaternion.rotation_matrix

    @property
    def quaternion(self) -> Quaternion:
        """Get the quaternion represented by this orientation."""
        return self._quaternion

    def __repr__(self) -> str:
        return "Orientation(rot_x={},rot_y={},rot_z={})".format(
            self.rot_x, self.rot_y, self.rot_z
        )
