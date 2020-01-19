from pathlib import Path
from typing import Optional

from cv2 import VideoCapture, imread
from numpy import ndarray

from .base import BaseCamera


class ImageFileCamera(BaseCamera):
    def __init__(
        self, image_path: Path, *, calibration_file: Optional[Path] = None
    ) -> None:
        self.image_path = image_path
        super().__init__(calibration_file=calibration_file)

    def capture_frame(self) -> ndarray:
        return imread(str(self.image_path))


class VideoFileCamera(BaseCamera):
    def __init__(
        self, video_path: Path, *, calibration_file: Optional[Path] = None
    ) -> None:
        super().__init__(calibration_file=calibration_file)
        self.video_capture = self.get_video_capture(video_path)

    def get_video_capture(self, video_path: Path) -> VideoCapture:
        return VideoCapture(str(video_path))

    def capture_frame(self) -> ndarray:
        _, frame = self.video_capture.read()
        return frame

    def close(self) -> None:
        super().close()
        self.video_capture.release()
