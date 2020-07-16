from pathlib import Path
from typing import Any, Callable

import pytest

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR, get_calibration
from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_type import MarkerType


@pytest.fixture(params=IMAGE_DATA.keys())
def image_camera(request: Any) -> ImageFileCamera:
    return ImageFileCamera(
        TEST_IMAGE_DIR.joinpath(request.param),
        marker_type=MarkerType.DICT_APRILTAG_36H11,
        marker_size=100,
    )


def test_capture_frame(benchmark: Callable, image_camera: ImageFileCamera) -> None:
    benchmark(image_camera.capture_frame)


def test_get_visible_markers(
    benchmark: Callable, image_camera: ImageFileCamera
) -> None:
    benchmark(image_camera.get_visible_markers)


def test_save_frame(
    benchmark: Callable,
    image_camera: ImageFileCamera,
    temp_image_file: Callable[[str], Path],
) -> None:
    benchmark(image_camera.save_frame, temp_image_file)


def test_save_frame_with_annotation(
    benchmark: Callable,
    image_camera: ImageFileCamera,
    temp_image_file: Callable[[str], Path],
) -> None:
    benchmark(image_camera.save_frame, temp_image_file, annotate=True)


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_process_frame(
    filename: str, benchmark: Callable, temp_image_file: Callable[[str], Path]
) -> None:
    camera = ImageFileCamera(
        TEST_IMAGE_DIR.joinpath(filename),
        marker_type=MarkerType.DICT_APRILTAG_36H11,
        marker_size=100,
    )
    benchmark(camera.save_frame, temp_image_file)


@pytest.mark.parametrize("filename,camera_name", IMAGE_DATA.items())
def test_process_frame_eager(
    filename: str,
    camera_name: str,
    benchmark: Callable,
    temp_image_file: Callable[[str], Path],
) -> None:
    camera = ImageFileCamera(
        TEST_IMAGE_DIR.joinpath(filename),
        calibration_file=get_calibration(camera_name),
        marker_type=MarkerType.DICT_APRILTAG_36H11,
        marker_size=100,
    )
    benchmark(camera.save_frame, temp_image_file)
