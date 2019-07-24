from typing import Optional

from attr import attrib, attrs
from cached_property import cached_property
from cv2 import aruco
from numpy import arctan2, array, linalg

from .calibration import CalibrationParameters
from .coords import Coordinates, Orientation, Spherical, ThreeDCoordinates
from .exceptions import MissingCalibrationsError


@attrs
class Marker:
    __id = attrib()  # type: int
    __pixel_corners = attrib()
    __size = attrib()  # type: int
    __camera_calibration_params = attrib(
        default=None
    )  # type: Optional[CalibrationParameters]
    __precalculated_vectors = attrib(default=None)
    __is_eager = attrib(default=False)  # type: bool

    @property  # noqa: A003
    def id(self):
        return self.__id

    @property
    def size(self):
        return self.__size

    def _is_eager(self):
        return self.__is_eager

    @cached_property
    def pixel_corners(self):
        return [Coordinates(*coords) for coords in self.__pixel_corners]

    @cached_property
    def pixel_centre(self):
        tl, _, br, _ = self.__pixel_corners
        return Coordinates([tl[0] + (self.__size / 2) - 1, br[1] - (self.__size / 2)])

    @cached_property
    def distance(self):
        return int(linalg.norm(self._tvec))

    @property
    def orientation(self):
        return Orientation(*self._rvec)

    @cached_property
    def spherical(self):
        x, y, z = self._tvec
        return Spherical(rot_x=arctan2(y, z), rot_y=arctan2(x, z), dist=self.distance)

    @property
    def cartesian(self):
        return ThreeDCoordinates(*self._tvec)

    def _get_pose_vectors(self, cache=True):
        if self.__precalculated_vectors is not None:
            return self.__precalculated_vectors

        if self.__camera_calibration_params is None:
            raise MissingCalibrationsError()

        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
            [self.__pixel_corners], self.__size, *self.__camera_calibration_params
        )
        if cache:
            self.__precalculated_vectors = (rvec[0][0], tvec[0][0])

        return self.__precalculated_vectors

    @property
    def _rvec(self):
        rvec, _ = self._get_pose_vectors()
        return rvec

    @property
    def _tvec(self):
        _, tvec = self._get_pose_vectors()
        return tvec

    def as_dict(self):
        marker_dict = {
            "id": self.id,
            "size": self.size,
            "pixel_corners": self.__pixel_corners.tolist(),
        }
        try:
            marker_dict.update(
                {"rvec": self._rvec.tolist(), "tvec": self._tvec.tolist()}
            )
        except MissingCalibrationsError:
            pass
        return marker_dict

    @classmethod
    def from_dict(cls, marker_dict):
        marker_args = [
            marker_dict["id"],
            array(marker_dict["pixel_corners"]),
            marker_dict["size"],
            None,
        ]
        if "rvec" in marker_dict and "tvec" in marker_dict:
            marker_args.append((array(marker_dict["rvec"]), array(marker_dict["tvec"])))
            marker_args.append(True)  # Mark the marker as eager
        return cls(*marker_args)
