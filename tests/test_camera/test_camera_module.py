import pytest

import zoloto.cameras
from zoloto.marker_type import MarkerType


def test_exposes_camera() -> None:
    assert zoloto.cameras.Camera == zoloto.cameras.camera.Camera


@pytest.mark.parametrize("camera_name", ["ImageFileCamera", "VideoFileCamera"])
def test_exposes_file_camera(camera_name) -> None:
    assert getattr(zoloto.cameras, camera_name) == getattr(
        zoloto.cameras.file, camera_name
    )


def test_camera_requires_marker_size() -> None:
    camera = zoloto.cameras.file.ImageFileCamera(
        "test.png", marker_type=MarkerType.DICT_4X4_100
    )
    with pytest.raises(ValueError):
        camera.get_marker_size(0)

    class TestCamera(zoloto.cameras.file.ImageFileCamera):
        def get_marker_size(self, marker_id: int) -> int:
            return 200

    camera = TestCamera("test.png", marker_type=MarkerType.DICT_4X4_100)
    assert camera.get_marker_size(0) == 200

    camera = zoloto.cameras.file.ImageFileCamera(
        "test.png", marker_type=MarkerType.DICT_4X4_100, marker_size=200,
    )
    assert camera.get_marker_size(0) == 200
