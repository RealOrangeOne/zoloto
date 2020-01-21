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
def test_gets_window_size_for_file_camera(filename: str) -> None:
    class TestCamera(ImageFileCamera):
        marker_dict = MarkerDict.DICT_APRILTAG_36H11

        def get_marker_size(self, marker_id: int) -> int:
            return 100

    image = Image.open(TEST_IMAGE_DIR.joinpath(filename))
    assert (
        CameraViewer.get_window_size(TestCamera(TEST_IMAGE_DIR.joinpath(filename),))
        == image.size
    )


@given(reasonable_image_size())
def test_gets_window_size_for_marker_camera(image_size: int) -> None:
    class TestCamera(MarkerCamera):
        marker_dict = MarkerDict.DICT_APRILTAG_36H11

    camera = TestCamera(0, marker_size=image_size)
    assert CameraViewer.get_window_size(camera) == camera.get_resolution()
