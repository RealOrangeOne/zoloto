import os

import pytest
from cv2.aruco import DICT_APRILTAG_36H11

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR, get_calibration
from zoloto.cameras.file import ImageFileCamera


@pytest.fixture(params=IMAGE_DATA.keys())
def image_camera(request):
    return ImageFileCamera(
        os.path.join(TEST_IMAGE_DIR, request.param), marker_dict=DICT_APRILTAG_36H11
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
        def get_marker_size(self, id):
            return 100

    camera = TestCamera(
        os.path.join(TEST_IMAGE_DIR, filename), marker_dict=DICT_APRILTAG_36H11
    )
    benchmark(camera.save_frame, temp_image_file)


@pytest.mark.parametrize("filename,detection_data", IMAGE_DATA.items())
def test_process_frame_eager(filename, detection_data, benchmark, temp_image_file):
    class TestCamera(ImageFileCamera):
        def get_marker_size(self, id):
            return 100

    camera = TestCamera(
        os.path.join(TEST_IMAGE_DIR, filename),
        marker_dict=DICT_APRILTAG_36H11,
        calibration_file=get_calibration(detection_data["camera"]),
    )
    benchmark(camera.save_frame, temp_image_file)
