import pytest
from hypothesis import given
from PIL import Image

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR
from tests.strategies import reasonable_image_size
from zoloto.cameras import ImageFileCamera
from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MarkerType
from zoloto.viewer import CameraViewer


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_gets_window_size_for_file_camera(filename: str) -> None:
    image = Image.open(TEST_IMAGE_DIR.joinpath(filename))
    assert (
        CameraViewer.get_window_size(
            ImageFileCamera(
                TEST_IMAGE_DIR.joinpath(filename),
                marker_type=MarkerType.DICT_APRILTAG_36H11,
                marker_size=100,
            )
        )
        == image.size
    )


@given(reasonable_image_size())
def test_gets_window_size_for_marker_camera(image_size: int) -> None:
    camera = MarkerCamera(
        0, marker_size=image_size, marker_type=MarkerType.DICT_APRILTAG_36H11
    )
    assert CameraViewer.get_window_size(camera) == camera.get_resolution()
