from typing import Any, Tuple, Optional, Dict, List, cast

from cached_property import cached_property
from cv2 import aruco
from fastcache import clru_cache
from numpy import arctan2, array, linalg

from .calibration import CalibrationParameters
from .coords import Coordinates, Orientation, Spherical, ThreeDCoordinates
from .exceptions import MissingCalibrationsError

from numpy import ndarray


class Marker:
    def __init__(
        self,
        marker_id: int,
        corners: ndarray[Tuple[float, float]],
        size: int,
        calibration_params: Optional[CalibrationParameters] = None,
        precalculated_vectors: Optional[Tuple[float, float]] = None,
    ) -> None:
        self.__id = marker_id
        self.__pixel_corners = corners
        self.__size = size
        self.__camera_calibration_params = calibration_params
        self.__precalculated_vectors = precalculated_vectors

    @property  # noqa: A003
    def id(self) -> int:
        return self.__id

    @property
    def size(self) -> int:
        return self.__size

    def _is_eager(self) -> bool:
        return self.__precalculated_vectors is not None

    @property
    def pixel_corners(self) -> List:
        return [Coordinates(*coords) for coords in self.__pixel_corners]

    @cached_property  # type: ignore
    def pixel_centre(self) -> Coordinates:
        tl, _, br, _ = self.__pixel_corners
        return Coordinates(*[tl[0] + (self.__size / 2) - 1, br[1] - (self.__size / 2)])

    @cached_property  # type: ignore
    def distance(self) -> int:
        return int(linalg.norm(self._tvec))

    @property
    def orientation(self) -> Orientation:
        return Orientation(*self._rvec)

    @cached_property  # type: ignore
    def spherical(self) -> Spherical:
        x, y, z = self._tvec
        return Spherical(rot_x=arctan2(y, z), rot_y=arctan2(x, z), dist=self.distance)

    @property
    def cartesian(self) -> ThreeDCoordinates:
        return ThreeDCoordinates(*self._tvec)

    @clru_cache(maxsize=None)  # type: ignore
    def _get_pose_vectors(self) -> Tuple[Any, Any]:
        if self._is_eager():
            return cast(Tuple[Any, Any], self.__precalculated_vectors)

        if self.__camera_calibration_params is None:
            raise MissingCalibrationsError()

        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
            [self.__pixel_corners], self.__size, *self.__camera_calibration_params
        )
        return rvec[0][0], tvec[0][0]

    @property
    def _rvec(self) -> ndarray:
        rvec, _ = self._get_pose_vectors()
        return rvec

    @property
    def _tvec(self) -> ndarray:
        _, tvec = self._get_pose_vectors()
        return tvec

    def as_dict(self) -> Dict[str, Any]:
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
    def from_dict(cls, marker_dict: Dict[str, Any]) -> "Marker":
        marker_args = [
            marker_dict["id"],
            array(marker_dict["pixel_corners"]),
            marker_dict["size"],
            None,
        ]
        if "rvec" in marker_dict and "tvec" in marker_dict:
            marker_args.append((array(marker_dict["rvec"]), array(marker_dict["tvec"])))
        return cls(*marker_args)
