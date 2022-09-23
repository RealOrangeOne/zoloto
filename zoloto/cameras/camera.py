from pathlib import Path
from typing import Any, Generator, Optional, Tuple

from cv2 import CAP_PROP_BUFFERSIZE, VideoCapture
from numpy.typing import NDArray

from zoloto.marker_type import MarkerType

from .base import BaseCamera
from .mixins import IterableCameraMixin, VideoCaptureMixin, ViewableCameraMixin
from .utils import (
    get_video_capture_resolution,
    set_video_capture_resolution,
    validate_calibrated_video_capture_resolution,
)


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


class Camera(VideoCaptureMixin, IterableCameraMixin, BaseCamera, ViewableCameraMixin):
    def __init__(
        self,
        camera_id: int,
        *,
        marker_size: Optional[int] = None,
        marker_type: MarkerType,
        calibration_file: Optional[Path] = None,
        resolution: Optional[Tuple[int, int]] = None,
    ) -> None:
        super().__init__(
            marker_size=marker_size,
            marker_type=marker_type,
            calibration_file=calibration_file,
        )
        self.camera_id = camera_id
        self.video_capture = self.get_video_capture(self.camera_id)

        if resolution is not None:
            self._set_resolution(resolution)

        if self.calibration_params is not None:
            validate_calibrated_video_capture_resolution(
                self.video_capture,
                self.calibration_params,
                override=resolution is not None,
            )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.camera_id}>"

    def get_video_capture(self, camera_id: int) -> VideoCapture:
        cap = VideoCapture(camera_id)
        cap.set(CAP_PROP_BUFFERSIZE, 1)
        return cap

    def _set_resolution(self, resolution: Tuple[int, int]) -> None:
        set_video_capture_resolution(self.video_capture, resolution)

    def get_resolution(self) -> Tuple[int, int]:
        return get_video_capture_resolution(self.video_capture)

    def capture_frame(self) -> NDArray:
        # Hack: Double capture frames to fill buffer.
        self.video_capture.read()
        return super().capture_frame()

    def close(self) -> None:
        super().close()
        self.video_capture.release()

    @classmethod
    def discover(cls, **kwargs: Any) -> Generator["Camera", None, None]:
        for camera_id in find_camera_ids():
            yield cls(camera_id, **kwargs)


class SnapshotCamera(VideoCaptureMixin, BaseCamera):
    """
    A modified version of Camera optimised for single use.

    - Doesn't keep the camera open between captures
    """

    def __init__(
        self,
        camera_id: int,
        *,
        marker_size: Optional[int] = None,
        marker_type: MarkerType,
        calibration_file: Optional[Path] = None,
        resolution: Optional[Tuple[int, int]] = None,
    ) -> None:
        super().__init__(
            marker_size=marker_size,
            marker_type=marker_type,
            calibration_file=calibration_file,
        )
        self.camera_id = camera_id
        self._resolution = resolution

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.camera_id}>"

    def get_video_capture(self, camera_id: int) -> VideoCapture:
        video_capture = VideoCapture(camera_id)
        if self._resolution is not None:
            set_video_capture_resolution(video_capture, self._resolution)
        else:
            self._resolution = get_video_capture_resolution(video_capture)

        if self.calibration_params is not None:
            validate_calibrated_video_capture_resolution(
                video_capture, self.calibration_params, override=False
            )
        return video_capture

    def get_resolution(self) -> Tuple[int, int]:
        if self._resolution is None:
            raise ValueError(
                "Cannot find resolution of camera until at least 1 frame has been captured."
            )
        return self._resolution

    def capture_frame(self) -> NDArray:
        self.video_capture = self.get_video_capture(self.camera_id)
        frame = super().capture_frame()
        self.video_capture.release()
        return frame

    @classmethod
    def discover(cls, **kwargs: Any) -> Generator["SnapshotCamera", None, None]:
        for camera_id in find_camera_ids():
            yield cls(camera_id, **kwargs)
