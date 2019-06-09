import json
import os

import pytest
from cv2.aruco import DICT_APRILTAG_36H11

from yuri.cameras.file import ImageFileCamera

TEST_DATA_DIR = "tests/images/"

with open(os.path.join(TEST_DATA_DIR, "markers.json")) as f:
    image_data = json.load(f)


def test_has_data_for_all_images():
    assert len(image_data) == len(os.listdir(TEST_DATA_DIR)) - 1
    for filename in image_data.keys():
        assert os.path.exists(os.path.join(TEST_DATA_DIR, filename))


@pytest.mark.parametrize("filename,detection_data", image_data.items())
def test_detects_marker_ids(filename, detection_data):
    camera = ImageFileCamera(
        os.path.join(TEST_DATA_DIR, filename), marker_dict=DICT_APRILTAG_36H11
    )
    assert sorted(camera.get_visible_markers()) == sorted(detection_data["markers"])


@pytest.mark.parametrize("filename", image_data.keys())
def test_annotates_frame(filename, make_temp_file):
    output_file = make_temp_file(".png")
    camera = ImageFileCamera(
        os.path.join(TEST_DATA_DIR, filename), marker_dict=DICT_APRILTAG_36H11
    )
    camera.save_frame(output_file, annotate=True)


@pytest.mark.parametrize("filename,detection_data", image_data.items())
def test_gets_markers(filename, detection_data):
    class TestCamera(ImageFileCamera):
        def get_marker_size(self, id):
            return 100

        def get_calibrations(self):
            return None

    camera = TestCamera(
        os.path.join(TEST_DATA_DIR, filename), marker_dict=DICT_APRILTAG_36H11
    )
    markers = list(camera.process_frame())
    assert len(markers) == len(detection_data["markers"])
    marker_ids = [marker.id for marker in markers]
    assert sorted(marker_ids) == sorted(detection_data["markers"])
    marker_sizes = {marker.size for marker in markers}
    assert marker_sizes == {100}
