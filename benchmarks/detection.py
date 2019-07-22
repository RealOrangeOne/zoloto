import pytest

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR, get_calibration
from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_dict import MarkerDict


@pytest.fixture(params=IMAGE_DATA.keys())
def image_camera(request):
    return ImageFileCamera(
        TEST_IMAGE_DIR.joinpath(request.param),
        marker_dict=MarkerDict.DICT_APRILTAG_36H11,
    )


def test_capture_frame(benchmark, image_camera):
    benchmark(image_camera.capture_frame)


def test_get_visible_markers(benchmark, image_camera):
    benchmark(image_camera.get_visible_markers)


def test_save_frame(benchmark, image_camera, temp_image_file):
    benchmark(image_camera.save_frame, temp_image_file)


def test_save_frame_with_annotation(benchmark, image_camera, temp_image_file):
    benchmark(image_camera.save_frame, temp_image_file, annotate=True)


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_process_frame(filename, benchmark, temp_image_file):
    class TestCamera(ImageFileCamera):
        def get_marker_size(self, marker_id):
            return 100

    camera = TestCamera(
        TEST_IMAGE_DIR.joinpath(filename), marker_dict=MarkerDict.DICT_APRILTAG_36H11
    )
    benchmark(camera.save_frame, temp_image_file)


@pytest.mark.parametrize("filename,camera_name", IMAGE_DATA.items())
def test_process_frame_eager(filename, camera_name, benchmark, temp_image_file):
    class TestCamera(ImageFileCamera):
        def get_marker_size(self, marker_id):
            return 100

    camera = TestCamera(
        TEST_IMAGE_DIR.joinpath(filename),
        marker_dict=MarkerDict.DICT_APRILTAG_36H11,
        calibration_file=get_calibration(camera_name),
    )
    benchmark(camera.save_frame, temp_image_file)
