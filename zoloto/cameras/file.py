from pathlib import Path
from typing import Generator, Optional

from cv2 import VideoCapture, imread
from numpy import ndarray

from zoloto.exceptions import CameraReadError

from .base import BaseCamera
from .mixins import IterableCameraMixin, VideoCaptureMixin


class ImageFileCamera(BaseCamera):
    def __init__(
        self, image_path: Path, *, calibration_file: Optional[Path] = None
    ) -> None:
        self.image_path = image_path
        super().__init__(calibration_file=calibration_file)

    def capture_frame(self) -> ndarray:
        return imread(str(self.image_path))


class VideoFileCamera(VideoCaptureMixin, BaseCamera, IterableCameraMixin):
    def __init__(
        self, video_path: Path, *, calibration_file: Optional[Path] = None
    ) -> None:
        super().__init__(calibration_file=calibration_file)
        self.video_capture = self.get_video_capture(video_path)

    def get_video_capture(self, video_path: Path) -> VideoCapture:
        return VideoCapture(str(video_path))

    def close(self) -> None:
        super().close()
        self.video_capture.release()

    def __iter__(self) -> Generator[ndarray, None, None]:
        try:
            yield from super().__iter__()
        except CameraReadError as e:
            if e.frame is not None:
                raise
