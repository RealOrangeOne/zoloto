from itertools import groupby
from pathlib import Path
from typing import List, Optional, Tuple, Iterator, Any

import cv2

from zoloto.calibration import parse_calibration_file, CalibrationParameters
from zoloto.exceptions import MissingCalibrationsError
from zoloto.marker import Marker
from zoloto.marker_dict import MarkerDict

from numpy import ndarray


class BaseCamera:
    def __init__(
        self, *, marker_dict: MarkerDict, calibration_file: Optional[Path] = None
    ):
        self.marker_dictionary = cv2.aruco.getPredefinedDictionary(marker_dict)
        self.calibration_file = calibration_file
        self.detector_params = self.get_detector_params(
            cv2.aruco.DetectorParameters_create()
        )

    def get_calibrations(self) -> Optional[CalibrationParameters]:
        if self.calibration_file is None:
            return None
        return parse_calibration_file(self.calibration_file)

    def get_detector_params(
        self, params: CalibrationParameters
    ) -> CalibrationParameters:
        return params

    def get_marker_size(self, marker_id: int) -> int:  # pragma: no cover
        raise NotImplementedError()

    def capture_frame(self) -> ndarray:  # pragma: no cover
        raise NotImplementedError()

    def save_frame(
        self, filename: Path, *, annotate: bool = False, frame: ndarray = None
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

    def _get_raw_ids_and_corners(
        self, frame: ndarray
    ) -> Tuple[List[List[int]], List[List[int]]]:
        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, self.marker_dictionary, parameters=self.detector_params
        )
        return ids, corners

    def _get_ids_and_corners(
        self, frame: ndarray = None
    ) -> Tuple[List[int], List[Any]]:
        if frame is None:
            frame = self.capture_frame()
        marker_ids, corners = self._get_raw_ids_and_corners(frame)
        if marker_ids is None:
            return [], []
        return [marker_id[0] for marker_id in marker_ids], [c[0] for c in corners]

    def _get_marker(
        self,
        marker_id: int,
        corners: List[Tuple[float, float]],
        calibration_params: Optional[CalibrationParameters],
    ) -> Marker:
        return Marker(
            marker_id, corners, self.get_marker_size(marker_id), calibration_params
        )

    def _get_eager_marker(
        self,
        marker_id: int,
        corners: List[Tuple[float, float]],
        size: int,
        calibration_params: Optional[CalibrationParameters],
        tvec: float,
        rvec: float,
    ) -> Marker:
        return Marker(marker_id, corners, size, calibration_params, (rvec, tvec))

    def process_frame(self, *, frame: ndarray = None) -> Iterator[Marker]:
        ids, corners = self._get_ids_and_corners(frame)
        calibration_params = self.get_calibrations()
        for corners, marker_id in zip(corners, ids):
            yield self._get_marker(int(marker_id), corners, calibration_params)

    def process_frame_eager(self, *, frame: ndarray = None) -> Iterator[Marker]:
        calibration_params = self.get_calibrations()
        if not calibration_params:
            raise MissingCalibrationsError()
        ids, corners = self._get_ids_and_corners(frame)

        def get_marker_size(id_and_corners: Tuple[int, Any]) -> int:
            return self.get_marker_size(id_and_corners[0])

        sorted_corners = sorted(zip(ids, corners), key=get_marker_size)
        for size, ids_and_corners in groupby(sorted_corners, get_marker_size):
            ids, corners = zip(*ids_and_corners)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, size, *calibration_params
            )
            for marker_id, corners, tvec, rvec in zip(ids, corners, tvecs, rvecs):
                yield self._get_eager_marker(
                    int(marker_id), corners, size, calibration_params, tvec[0], rvec[0]
                )

    def get_visible_markers(self, *, frame: ndarray = None) -> List[int]:
        ids, _ = self._get_ids_and_corners(frame)
        return ids

    def close(self) -> None:
        pass

    def __enter__(self) -> "BaseCamera":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()
