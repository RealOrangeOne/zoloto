import os

import pytest

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR, get_calibration
from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_dict import MarkerDict


def test_has_data_for_all_images():
    assert len(IMAGE_DATA) == len(os.listdir(TEST_IMAGE_DIR)) - 1
    for filename in IMAGE_DATA.keys():
        assert os.path.exists(os.path.join(TEST_IMAGE_DIR, filename))


@pytest.mark.parametrize("filename,detection_data", IMAGE_DATA.items())
def test_detects_marker_ids(filename, detection_data):
    camera = ImageFileCamera(
        os.path.join(TEST_IMAGE_DIR, filename),
        marker_dict=MarkerDict.DICT_APRILTAG_36H11,
    )
    assert sorted(camera.get_visible_markers()) == sorted(detection_data["markers"])


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_annotates_frame(filename, temp_image_file):
    camera = ImageFileCamera(
        os.path.join(TEST_IMAGE_DIR, filename),
        marker_dict=MarkerDict.DICT_APRILTAG_36H11,
    )
    camera.save_frame(temp_image_file, annotate=True)


@pytest.mark.parametrize("filename,detection_data", IMAGE_DATA.items())
def test_gets_markers(filename, detection_data):
    class TestCamera(ImageFileCamera):
        def get_marker_size(self, id):
            return 100

    camera = TestCamera(
        os.path.join(TEST_IMAGE_DIR, filename),
        marker_dict=MarkerDict.DICT_APRILTAG_36H11,
    )
    markers = list(camera.process_frame())
    assert len(markers) == len(detection_data["markers"])
    marker_ids = [marker.id for marker in markers]
    assert sorted(marker_ids) == sorted(detection_data["markers"])
    assert {marker.size for marker in markers} == {100}


@pytest.mark.parametrize("filename,detection_data", IMAGE_DATA.items())
def test_gets_marker_eager(filename, detection_data):
    class TestCamera(ImageFileCamera):
        def get_marker_size(self, id):
            return 100

    camera = TestCamera(
        os.path.join(TEST_IMAGE_DIR, filename),
        marker_dict=MarkerDict.DICT_APRILTAG_36H11,
        calibration_file=get_calibration(detection_data["camera"]),
    )
    markers = list(camera.process_frame_eager())
    assert sorted(marker.id for marker in markers) == sorted(detection_data["markers"])
    assert {marker.size for marker in markers} == {100}
