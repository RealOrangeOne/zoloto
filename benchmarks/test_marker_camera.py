import pytest
from cv2 import aruco

from yuri.camera import MarkerCamera


@pytest.fixture
def marker_camera():
    return MarkerCamera(25, marker_dict=aruco.DICT_6X6_50, marker_size=200)


def test_process_frame_eager(benchmark, marker_camera):
    frame = marker_camera.capture_frame()
    benchmark(lambda: list(marker_camera.process_frame_eager(frame)))


def test_process_frame(benchmark, marker_camera):
    frame = marker_camera.capture_frame()
    benchmark(lambda: list(marker_camera.process_frame(frame)))


def test_capture_frame(benchmark, marker_camera):
    benchmark(marker_camera.capture_frame)


def test_get_visible_markers(benchmark, marker_camera):
    frame = marker_camera.capture_frame()
    benchmark(marker_camera.get_visible_markers, frame=frame)
