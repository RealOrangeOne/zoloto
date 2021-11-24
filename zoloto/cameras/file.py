from pathlib import Path
from typing import Generator, Optional

from cv2 import VideoCapture, imread
from numpy import ndarray

from zoloto.exceptions import CameraOpenError, CameraReadError
from zoloto.marker_type import MarkerType

from .base import BaseCamera
from .mixins import IterableCameraMixin, VideoCaptureMixin, ViewableCameraMixin


class ImageFileCamera(BaseCamera):
    def __init__(
        self,
        image_path: Path,
        *,
        marker_size: Optional[int] = None,
        marker_type: MarkerType,
        calibration_file: Optional[Path] = None,
    ) -> None:
        super().__init__(
            marker_size=marker_size,
            marker_type=marker_type,
            calibration_file=calibration_file,
        )
        self.image_path = image_path
        self._frame = imread(str(self.image_path))

        if self._frame is None:
            raise CameraOpenError(f"Failed to read file {self.image_path}")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.image_path}>"

    def capture_frame(self) -> ndarray:
        return self._frame


class VideoFileCamera(
    VideoCaptureMixin, IterableCameraMixin, BaseCamera, ViewableCameraMixin
):
    def __init__(
        self,
        video_path: Path,
        *,
        marker_size: Optional[int] = None,
        marker_type: MarkerType,
        calibration_file: Optional[Path] = None,
    ) -> None:
        super().__init__(
            marker_size=marker_size,
            marker_type=marker_type,
            calibration_file=calibration_file,
        )
        self.video_path = video_path
        self.video_capture = VideoCapture(str(self.video_path))

        if not self.video_capture.isOpened():
            raise CameraOpenError(f"Failed to read file {self.video_path}")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.video_path}>"

    def close(self) -> None:
        super().close()
        self.video_capture.release()

    def __iter__(self) -> Generator[ndarray, None, None]:
        try:
            yield from super().__iter__()
        except CameraReadError as e:
            if e.frame is not None:
                raise
