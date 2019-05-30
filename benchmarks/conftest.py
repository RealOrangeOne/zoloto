import pytest
from cv2 import aruco

from yuri.camera import MarkerCamera


@pytest.fixture
def marker_camera():
    return MarkerCamera(25, marker_dict=aruco.DICT_6X6_50, marker_size=200)


@pytest.fixture
def marker(marker_camera):
    return next(marker_camera.process_frame())
