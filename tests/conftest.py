import json
import os
from tempfile import mkstemp

import pytest
from cv2 import aruco

from zoloto.calibration import get_fake_calibration_parameters
from zoloto.cameras.marker import MarkerCamera

TEST_DATA_DIR = "tests/images/"

with open(os.path.join(TEST_DATA_DIR, "markers.json")) as f:
    IMAGE_DATA = json.load(f)


@pytest.fixture
def make_temp_file(request):
    temp_file = None

    def clean_temp_file():
        nonlocal temp_file
        if temp_file is not None:
            os.remove(temp_file)

    def _make_temp_file(*args, **kwargs):
        nonlocal temp_file
        handle, temp_file = mkstemp(*args, **kwargs)
        os.close(handle)
        return temp_file

    request.addfinalizer(clean_temp_file)
    return _make_temp_file


@pytest.fixture
def temp_image_file(make_temp_file):
    return make_temp_file(".png")


@pytest.fixture
def marker_camera():
    return MarkerCamera(25, marker_dict=aruco.DICT_6X6_50, marker_size=200)


@pytest.fixture
def marker(marker_camera):
    return next(marker_camera.process_frame())


@pytest.fixture
def fake_calibration_params():
    return get_fake_calibration_parameters(200)
