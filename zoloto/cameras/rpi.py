from pathlib import Path
from typing import Optional

from numpy.typing import NDArray

import picamera
import picamera.array
from zoloto.marker_type import MarkerType

from .base import BaseCamera
from .mixins import IterableCameraMixin, ViewableCameraMixin


class PiCamera(IterableCameraMixin, BaseCamera, ViewableCameraMixin):
    def __init__(
        self,
        *,
        marker_size: Optional[int] = None,
        marker_type: MarkerType,
        calibration_file: Optional[Path] = None
    ) -> None:
        super().__init__(
            marker_size=marker_size,
            marker_type=marker_type,
            calibration_file=calibration_file,
        )
        self.camera = picamera.PiCamera()

    def capture_frame(self) -> NDArray:
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

    def capture_frame(self) -> NDArray:
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as raw_capture:
                camera.capture(raw_capture, format="bgr")
                return raw_capture.array

    def close(self) -> None:
        super().close()
