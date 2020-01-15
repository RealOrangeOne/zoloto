import pytest
from hypothesis import given
from PIL import Image

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR
from tests.strategies import reasonable_image_size
from zoloto.cameras import ImageFileCamera
from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_dict import MarkerDict
from zoloto.viewer import CameraViewer


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_gets_window_size_for_file_camera(filename):
    image = Image.open(TEST_IMAGE_DIR.joinpath(filename))
    assert (
        CameraViewer.get_window_size(
            ImageFileCamera(
                TEST_IMAGE_DIR.joinpath(filename),
                marker_dict=MarkerDict.DICT_APRILTAG_36H11,
            )
        )
        == image.size
    )


@given(reasonable_image_size())
def test_gets_window_size_for_marker_camera(image_size):
    camera = MarkerCamera(
        0, marker_dict=MarkerDict.DICT_APRILTAG_36H11, marker_size=image_size
    )
    assert CameraViewer.get_window_size(camera) == camera.get_resolution()
