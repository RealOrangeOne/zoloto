import os

import pytest
from cv2.aruco import DICT_APRILTAG_36H11

from tests.conftest import IMAGE_DATA, TEST_DATA_DIR
from yuri.cameras.file import ImageFileCamera


@pytest.fixture(params=IMAGE_DATA.keys())
def image_camera(request):
    return ImageFileCamera(
        os.path.join(TEST_DATA_DIR, request.param), marker_dict=DICT_APRILTAG_36H11
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

        def get_calibrations(self):
            return None

    camera = TestCamera(
        os.path.join(TEST_DATA_DIR, filename), marker_dict=DICT_APRILTAG_36H11
    )
    benchmark(camera.save_frame, temp_image_file)
