from abc import ABC, abstractmethod
from itertools import groupby
from pathlib import Path
from typing import Any, Generator, List, Optional, Tuple, TypeVar, Union, cast

import cv2
from numpy import ndarray

from zoloto.calibration import CalibrationParameters, parse_calibration_file
from zoloto.exceptions import MissingCalibrationsError
from zoloto.marker import EagerMarker, Marker, UncalibratedMarker
from zoloto.marker_type import MarkerType

T = TypeVar("T", bound="BaseCamera")


class BaseCamera(ABC):
    def __init__(
        self,
        *,
        marker_size: Optional[int] = None,
        marker_type: MarkerType,
        calibration_file: Optional[Path] = None
    ) -> None:
        self.calibration_file = calibration_file
        self.marker_type = marker_type
        self.marker_dictionary = cv2.aruco.getPredefinedDictionary(self.marker_type)
        self._marker_size = marker_size
        self.detector_params = self.get_detector_params()

    def get_calibrations(self) -> Optional[CalibrationParameters]:
        if self.calibration_file is None:
            return None
        return parse_calibration_file(self.calibration_file)

    def get_detector_params(self) -> cv2.aruco_DetectorParameters:
        return cv2.aruco.DetectorParameters_create()

    def get_marker_size(self, marker_id: int) -> int:
        if self._marker_size is None:
            raise ValueError(
                "`marker_size` should be passed in to the camera constructor, or override `get_marker_size`"
            )
        return self._marker_size

    @abstractmethod
    def capture_frame(self) -> ndarray:  # pragma: nocover
        raise NotImplementedError()

    def save_frame(
        self, filename: Path, *, annotate: bool = False, frame: Optional[ndarray] = None
    ) -> ndarray:
        if frame is None:
            frame = self.capture_frame()
        if annotate:
            self._annotate_frame(frame)
        cv2.imwrite(str(filename), frame)
        return frame

    def _annotate_frame(self, frame: ndarray) -> None:
        ids, corners = self._get_raw_ids_and_corners(frame)
        if corners:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    def _get_raw_ids_and_corners(self, frame: ndarray) -> Tuple[ndarray, ndarray]:
        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, self.marker_dictionary, parameters=self.detector_params
        )
        return ids, corners

    def _get_ids_and_corners(
        self, frame: Optional[ndarray] = None
    ) -> Tuple[List[int], List[ndarray]]:
        if frame is None:
            frame = self.capture_frame()
        marker_ids, corners = self._get_raw_ids_and_corners(frame)
        if marker_ids is None:
            return [], []
        return [marker_id[0] for marker_id in marker_ids], [c[0] for c in corners]

    def _get_marker(
        self,
        marker_id: int,
        corners: List[ndarray],
        calibration_params: Optional[CalibrationParameters],
    ) -> Union[UncalibratedMarker, Marker]:
        if calibration_params is None:
            return UncalibratedMarker(
                marker_id, corners, self.get_marker_size(marker_id), self.marker_type
            )
        return Marker(
            marker_id,
            corners,
            self.get_marker_size(marker_id),
            self.marker_type,
            calibration_params,
        )

    def _get_eager_marker(
        self,
        marker_id: int,
        corners: List[ndarray],
        size: int,
        tvec: ndarray,
        rvec: ndarray,
    ) -> EagerMarker:
        return EagerMarker(marker_id, corners, size, self.marker_type, (rvec, tvec))

    def process_frame(
        self, *, frame: Optional[ndarray] = None
    ) -> Generator[Union[UncalibratedMarker, Marker], None, None]:
        ids, corners = self._get_ids_and_corners(frame)
        calibration_params = self.get_calibrations()
        for marker_corners, marker_id in zip(corners, ids):
            yield self._get_marker(
                int(marker_id), cast(list, marker_corners), calibration_params
            )

    def process_frame_eager(
        self, *, frame: Optional[ndarray] = None
    ) -> Generator[EagerMarker, None, None]:
        calibration_params = self.get_calibrations()
        if not calibration_params:
            raise MissingCalibrationsError()
        ids, corners = self._get_ids_and_corners(frame)

        def get_marker_size(id_and_corners: Tuple[int, ndarray]) -> int:
            return self.get_marker_size(id_and_corners[0])

        sorted_corners = sorted(zip(ids, corners), key=get_marker_size)
        for size, ids_and_corners in groupby(sorted_corners, get_marker_size):
            size_ids, size_corners = zip(*ids_and_corners)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                size_corners, size, *calibration_params
            )
            for marker_id, marker_corners, tvec, rvec in zip(
                size_ids, size_corners, tvecs, rvecs
            ):
                yield self._get_eager_marker(
                    int(marker_id), marker_corners, size, tvec[0], rvec[0]
                )

    def get_visible_markers(self, *, frame: Optional[ndarray] = None) -> List[int]:
        ids, _ = self._get_ids_and_corners(frame)
        return [int(i) for i in ids]

    def close(self) -> None:
        pass

    def __enter__(self: T) -> T:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()
