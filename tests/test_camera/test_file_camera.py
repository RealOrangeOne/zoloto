from pathlib import Path

import pytest

from zoloto.cameras.file import ImageFileCamera, VideoFileCamera
from zoloto.exceptions import CameraOpenError
from zoloto.marker_type import MarkerType


def test_video_camera_unknown_file() -> None:
    with pytest.raises(CameraOpenError):
        VideoFileCamera(
            Path.cwd() / "missing.mp4", marker_type=MarkerType.APRILTAG_36H11
        )


def test_image_camera_unknown_file() -> None:
    with pytest.raises(CameraOpenError):
        ImageFileCamera(
            Path.cwd() / "missing.png", marker_type=MarkerType.APRILTAG_36H11
        )
