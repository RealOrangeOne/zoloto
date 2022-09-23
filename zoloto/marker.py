from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from cached_property import cached_property
from cv2 import aruco
from numpy import arctan2, linalg
from numpy.typing import NDArray

from zoloto.utils import cached_method

from .calibration import CalibrationParameters
from .coords import Coordinates, Orientation, Spherical, ThreeDCoordinates
from .exceptions import MissingCalibrationsError
from .marker_type import MarkerType


class BaseMarker(ABC):
    def __init__(
        self, marker_id: int, corners: List[NDArray], size: int, marker_type: MarkerType
    ):
        self.__id = marker_id
        self._pixel_corners = corners
        self.__size = size
        self.__marker_type = marker_type

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} size={self.size} type={self.marker_type.name}>"

    @abstractmethod
    def _get_pose_vectors(self) -> Tuple[NDArray, NDArray]:  # pragma: nocover
        raise NotImplementedError()

    @property  # noqa: A003
    def id(self) -> int:  # noqa: A003
        return self.__id

    @property
    def size(self) -> int:
        return self.__size

    @property
    def marker_type(self) -> MarkerType:
        return self.__marker_type

    @property
    def pixel_corners(self) -> List[Coordinates]:
        return [Coordinates(x=float(x), y=float(y)) for x, y in self._pixel_corners]

    @cached_property
    def pixel_centre(self) -> Coordinates:
        tl, _, br, _ = self.pixel_corners
        return Coordinates(
            x=tl.x + (self.size / 2) - 1,
            y=br.y - (self.size / 2),
        )

    @cached_property
    def distance(self) -> int:
        return int(linalg.norm(self._tvec))

    @cached_property
    def orientation(self) -> Orientation:
        return Orientation(*self._rvec)

    @cached_property
    def spherical(self) -> Spherical:
        x, y, z = self._tvec
        return Spherical(
            rot_x=float(arctan2(y, z)), rot_y=float(arctan2(x, z)), dist=self.distance
        )

    @property
    def cartesian(self) -> ThreeDCoordinates:
        return ThreeDCoordinates(*self._tvec.tolist())

    @property
    def _rvec(self) -> NDArray:
        return self._get_pose_vectors()[0]

    @property
    def _tvec(self) -> NDArray:
        return self._get_pose_vectors()[1]

    def as_dict(self) -> Dict[str, Any]:
        marker_dict = {
            "id": self.id,
            "size": self.size,
            "pixel_corners": [list(corner) for corner in self.pixel_corners],
        }
        try:
            marker_dict.update(
                {"rvec": self._rvec.tolist(), "tvec": self._tvec.tolist()}
            )
        except MissingCalibrationsError:
            pass
        return marker_dict


class EagerMarker(BaseMarker):
    def __init__(
        self,
        marker_id: int,
        corners: List[NDArray],
        size: int,
        marker_type: MarkerType,
        precalculated_vectors: Tuple[NDArray, NDArray],
    ):
        super().__init__(marker_id, corners, size, marker_type)
        self.__precalculated_vectors = precalculated_vectors

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} size={self.size} type={self.marker_type.name} distance={self.distance}>"

    def _get_pose_vectors(self) -> Tuple[NDArray, NDArray]:
        return self.__precalculated_vectors


class Marker(BaseMarker):
    def __init__(
        self,
        marker_id: int,
        corners: List[NDArray],
        size: int,
        marker_type: MarkerType,
        calibration_params: CalibrationParameters,
    ):
        super().__init__(marker_id, corners, size, marker_type)
        self.__calibration_params = calibration_params

    @cached_method
    def _get_pose_vectors(self) -> Tuple[NDArray, NDArray]:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
            [self._pixel_corners],
            self.size,
            self.__calibration_params.camera_matrix,
            self.__calibration_params.distance_coefficients,
        )
        return rvec[0][0], tvec[0][0]


class UncalibratedMarker(BaseMarker):
    def _get_pose_vectors(self) -> Tuple[NDArray, NDArray]:
        raise MissingCalibrationsError()
