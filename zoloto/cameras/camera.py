from pathlib import Path
from typing import Any, Generator, Optional

from cv2 import CAP_PROP_BUFFERSIZE, VideoCapture
from numpy import ndarray

from .base import BaseCamera


def find_camera_ids() -> Generator[int, None, None]:
    """
    Find and return ids of connected cameras.

    Works the same as VideoCapture(-1).
    """
    for camera_id in range(8):
        capture = VideoCapture(camera_id)
        opened = capture.isOpened()
        capture.release()
        if opened:
            yield camera_id


class Camera(BaseCamera):
    def __init__(
        self, camera_id: int, *, calibration_file: Optional[Path] = None
    ) -> None:
        super().__init__(calibration_file=calibration_file)
        self.camera_id = camera_id
        self.video_capture = self.get_video_capture(self.camera_id)

    def get_video_capture(self, camera_id: int) -> VideoCapture:
        cap = VideoCapture(camera_id)
        cap.set(CAP_PROP_BUFFERSIZE, 1)
        return cap

    def capture_frame(self) -> ndarray:
        # Hack: Double capture frames to fill buffer.
        self.video_capture.read()
        _, frame = self.video_capture.read()
        return frame

    def close(self) -> None:
        super().close()
        self.video_capture.release()

    @classmethod
    def discover(cls, **kwargs: Any) -> Generator["Camera", None, None]:
        for camera_id in find_camera_ids():
            yield cls(camera_id, **kwargs)


class SnapshotCamera(BaseCamera):
    """
    A modified version of Camera optimised for single use.

    - Doesn't keep the camera open between captures
    """

    def __init__(
        self, camera_id: int, *, calibration_file: Optional[Path] = None
    ) -> None:
        super().__init__(calibration_file=calibration_file)
        self.camera_id = camera_id

    def get_video_capture(self, camera_id: int) -> VideoCapture:
        return VideoCapture(camera_id)

    def capture_frame(self) -> ndarray:
        video_capture = self.get_video_capture(self.camera_id)
        _, frame = video_capture.read()
        video_capture.release()
        return frame

    @classmethod
    def discover(cls, **kwargs: Any) -> Generator["SnapshotCamera", None, None]:
        for camera_id in find_camera_ids():
            yield cls(camera_id, **kwargs)
