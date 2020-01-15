import json
import os
from pathlib import Path
from tempfile import mkstemp

import pytest
from hypothesis import settings as hypothesis_settings

from zoloto.calibration import get_fake_calibration_parameters
from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_dict import MarkerDict

TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
TEST_IMAGE_DIR = TEST_DATA_DIR.joinpath("images")
CALIBRATIONS_DIR = TEST_DATA_DIR.joinpath("calibrations")

IMAGE_DATA = json.loads(TEST_IMAGE_DIR.joinpath("images.json").read_text())

hypothesis_settings.register_profile("main", deadline=None)
hypothesis_settings.load_profile("main")


def get_calibration(camera: str):
    return CALIBRATIONS_DIR.joinpath(camera + ".xml")


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
    return MarkerCamera(25, marker_dict=MarkerDict.DICT_6X6_50, marker_size=200)


@pytest.fixture
def marker(marker_camera):
    return next(marker_camera.process_frame())


@pytest.fixture
def fake_calibration_params():
    return get_fake_calibration_parameters(200)
