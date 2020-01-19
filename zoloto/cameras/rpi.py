from pathlib import Path
from typing import Optional

from numpy import ndarray

import picamera
import picamera.array

from .base import BaseCamera


class PiCamera(BaseCamera):
    def __init__(self, *, calibration_file: Optional[Path] = None) -> None:
        super().__init__(calibration_file=calibration_file)
        self.camera = picamera.PiCamera()

    def capture_frame(self) -> ndarray:
        with picamera.array.PiRGBArray(self.camera) as raw_capture:
            self.camera.capture(raw_capture, format="bgr")
            return raw_capture.array

    def close(self) -> None:
        super().close()
        self.camera.close()


class PiSnapshotCamera(BaseCamera):
    """
    A modified version of PiCamera optimised for single use.

    - Doesn't keep the camera open between captures
    """

    def capture_frame(self) -> ndarray:
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as raw_capture:
                camera.capture(raw_capture, format="bgr")
                return raw_capture.array

    def close(self) -> None:
        super().close()
