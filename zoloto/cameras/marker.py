from pathlib import Path
from typing import Optional, Tuple

import cv2
from numpy import ndarray

from zoloto.calibration import CalibrationParameters, get_fake_calibration_parameters

from .base import BaseCamera


class MarkerCamera(BaseCamera):
    """
    A camera which always returns a single, full-screen marker
    """

    BORDER_SIZE = 40

    def __init__(
        self,
        marker_id: int,
        marker_size: int,
        *,
        calibration_file: Optional[Path] = None
    ) -> None:
        super().__init__(calibration_file=calibration_file)
        self.marker_id = marker_id
        self.marker_size = marker_size

    def get_marker_size(self, marker_id: int) -> int:
        return self.marker_size

    def get_calibrations(self) -> Optional[CalibrationParameters]:
        return get_fake_calibration_parameters(self.marker_size)

    def get_resolution(self) -> Tuple[int, int]:
        size = int(self.get_marker_size(self.marker_id) + self.BORDER_SIZE * 2)
        return size, size

    def capture_frame(self) -> ndarray:
        image = cv2.aruco.drawMarker(
            self.marker_dictionary, self.marker_id, self.marker_size
        )
        return cv2.copyMakeBorder(
            image,
            self.BORDER_SIZE,
            self.BORDER_SIZE,
            self.BORDER_SIZE,
            self.BORDER_SIZE,
            cv2.BORDER_CONSTANT,
            value=[255, 0, 0],
        )
