from typing import Any, Tuple

import cv2

from zoloto.calibration import get_fake_calibration_parameters, CalibrationParameters

from .base import BaseCamera

from numpy import ndarray


class MarkerCamera(BaseCamera):
    """
    A camera which always returns a single, full-screen marker
    """

    BORDER_SIZE = 40

    def __init__(self, marker_id: int, marker_size: int, **kwargs: Any):
        super().__init__(**kwargs)
        self.marker_id = marker_id
        self.marker_size = marker_size

    def get_marker_size(self, marker_id: int) -> int:
        return self.marker_size

    def get_calibrations(self) -> CalibrationParameters:
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
