from pathlib import Path
from typing import Generator, Optional, Tuple

from cv2 import VideoCapture, imread
from numpy.typing import NDArray

from zoloto.exceptions import CameraReadError
from zoloto.marker_type import MarkerType

from .base import BaseCamera
from .mixins import IterableCameraMixin, VideoCaptureMixin, ViewableCameraMixin
from .utils import (
    get_video_capture_resolution,
    validate_calibrated_video_capture_resolution,
)


class ImageFileCamera(BaseCamera):
    def __init__(
        self,
        image_path: Path,
        *,
        marker_size: Optional[int] = None,
        marker_type: MarkerType,
        calibration_file: Optional[Path] = None,
    ) -> None:
        self.image_path = image_path
        super().__init__(
            marker_size=marker_size,
            marker_type=marker_type,
            calibration_file=calibration_file,
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.image_path}>"

    def capture_frame(self) -> NDArray:
        return imread(str(self.image_path))


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

        if self.calibration_params is not None:
            validate_calibrated_video_capture_resolution(
                self.video_capture, self.calibration_params, override=False
            )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.video_path}>"

    def close(self) -> None:
        super().close()
        self.video_capture.release()

    def get_resolution(self) -> Tuple[int, int]:
        return get_video_capture_resolution(self.video_capture)

    def __iter__(self) -> Generator[NDArray, None, None]:
        try:
            yield from super().__iter__()
        except CameraReadError as e:
            if e.frame is not None:
                raise
