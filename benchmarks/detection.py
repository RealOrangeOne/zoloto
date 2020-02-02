from pathlib import Path
from typing import Any, Callable

import pytest

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR, get_calibration
from zoloto.cameras.file import ImageFileCamera as BaseImageFileCamera
from zoloto.marker_type import MarkerType


@pytest.fixture(params=IMAGE_DATA.keys())
def image_camera(request: Any) -> BaseImageFileCamera:
    class ImageFileCamera(BaseImageFileCamera):
        marker_type = MarkerType.DICT_APRILTAG_36H11

        def get_marker_size(self, marker_id: int) -> int:
            return 100

    return ImageFileCamera(TEST_IMAGE_DIR.joinpath(request.param))


def test_capture_frame(benchmark: Callable, image_camera: BaseImageFileCamera) -> None:
    benchmark(image_camera.capture_frame)


def test_get_visible_markers(
    benchmark: Callable, image_camera: BaseImageFileCamera
) -> None:
    benchmark(image_camera.get_visible_markers)


def test_save_frame(
    benchmark: Callable,
    image_camera: BaseImageFileCamera,
    temp_image_file: Callable[[str], Path],
) -> None:
    benchmark(image_camera.save_frame, temp_image_file)


def test_save_frame_with_annotation(
    benchmark: Callable,
    image_camera: BaseImageFileCamera,
    temp_image_file: Callable[[str], Path],
) -> None:
    benchmark(image_camera.save_frame, temp_image_file, annotate=True)


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_process_frame(
    filename: str, benchmark: Callable, temp_image_file: Callable[[str], Path]
) -> None:
    class TestCamera(BaseImageFileCamera):
        marker_type = MarkerType.DICT_APRILTAG_36H11

        def get_marker_size(self, marker_id: int) -> int:
            return 100

    camera = TestCamera(TEST_IMAGE_DIR.joinpath(filename))
    benchmark(camera.save_frame, temp_image_file)


@pytest.mark.parametrize("filename,camera_name", IMAGE_DATA.items())
def test_process_frame_eager(
    filename: str,
    camera_name: str,
    benchmark: Callable,
    temp_image_file: Callable[[str], Path],
) -> None:
    class TestCamera(BaseImageFileCamera):
        marker_type = MarkerType.DICT_APRILTAG_36H11

        def get_marker_size(self, marker_id: int) -> int:
            return 100

    camera = TestCamera(
        TEST_IMAGE_DIR.joinpath(filename),
        calibration_file=get_calibration(camera_name),
    )
    benchmark(camera.save_frame, temp_image_file)
