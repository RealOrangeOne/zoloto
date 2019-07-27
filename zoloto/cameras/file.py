from pathlib import Path

from cv2 import VideoCapture, imread

from .base import BaseCamera

from typing import Any

from numpy import ndarray


class ImageFileCamera(BaseCamera):
    def __init__(self, image_path: Path, **kwargs: Any) -> None:
        self.image_path = image_path
        super().__init__(**kwargs)

    def capture_frame(self) -> ndarray:
        return imread(str(self.image_path))


class VideoFileCamera(BaseCamera):
    def __init__(self, video_path: Path, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.video_capture = self.get_video_capture(video_path)

    def get_video_capture(self, video_path: Path) -> VideoCapture:
        return VideoCapture(str(video_path))

    def capture_frame(self) -> ndarray:
        _, frame = self.video_capture.read()
        return frame

    def close(self) -> None:
        super().close()
        self.video_capture.release()
