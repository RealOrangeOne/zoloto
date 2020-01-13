import operator

import pytest

from tests.conftest import IMAGE_DATA, TEST_IMAGE_DIR, get_calibration
from zoloto.cameras.file import ImageFileCamera as BaseImageFileCamera
from zoloto.marker_dict import MarkerDict


def test_has_data_for_all_images():
    assert len(IMAGE_DATA) == len(list(TEST_IMAGE_DIR.glob("*.jpg")))
    for filename in IMAGE_DATA.keys():
        assert TEST_IMAGE_DIR.joinpath(filename).exists()


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_detects_marker_ids(filename, snapshot):
    class ImageFileCamera(BaseImageFileCamera):
        marker_dict = MarkerDict.DICT_APRILTAG_36H11

    camera = ImageFileCamera(TEST_IMAGE_DIR.joinpath(filename),)
    snapshot.assert_match(sorted(camera.get_visible_markers()))


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_annotates_frame(filename, temp_image_file):
    class ImageFileCamera(BaseImageFileCamera):
        marker_dict = MarkerDict.DICT_APRILTAG_36H11

    camera = ImageFileCamera(TEST_IMAGE_DIR.joinpath(filename),)
    camera.save_frame(temp_image_file, annotate=True)


@pytest.mark.parametrize("filename", IMAGE_DATA.keys())
def test_gets_markers(filename, snapshot):
    class TestCamera(BaseImageFileCamera):
        marker_dict = MarkerDict.DICT_APRILTAG_36H11

        def get_marker_size(self, marker_id):
            return 100

    camera = TestCamera(TEST_IMAGE_DIR.joinpath(filename),)
    snapshot.assert_match(
        sorted(
            (
                {
                    "id": marker.id,
                    "size": marker.size,
                    "pixel_corners": [
                        coords.to_list() for coords in marker.pixel_corners
                    ],
                    "pixel_centre": marker.pixel_centre.to_list(),
                }
                for marker in camera.process_frame()
            ),
            key=operator.itemgetter("pixel_centre"),
        )
    )


@pytest.mark.parametrize("filename,camera_name", IMAGE_DATA.items())
def test_gets_markers_eager(filename, camera_name, snapshot):
    class TestCamera(BaseImageFileCamera):
        marker_dict = MarkerDict.DICT_APRILTAG_36H11

        def get_marker_size(self, marker_id):
            return 100

    camera = TestCamera(
        TEST_IMAGE_DIR.joinpath(filename),
        calibration_file=get_calibration(camera_name),
    )
    snapshot.assert_match(
        sorted(
            (
                {
                    "id": marker.id,
                    "size": marker.size,
                    "pixel_corners": [
                        coords.to_list() for coords in marker.pixel_corners
                    ],
                    "pixel_centre": marker.pixel_centre.to_list(),
                    "distance": marker.distance,
                    "orientation": tuple(marker.orientation),
                    "spherical": tuple(marker.spherical),
                    "cartesian": marker.cartesian.to_list(),
                }
                for marker in camera.process_frame_eager()
            ),
            key=operator.itemgetter("pixel_centre"),
        )
    )


@pytest.mark.parametrize("filename,camera_name", IMAGE_DATA.items())
def test_gets_markers_with_calibration(filename, camera_name, snapshot):
    class TestCamera(BaseImageFileCamera):
        marker_dict = MarkerDict.DICT_APRILTAG_36H11

        def get_marker_size(self, marker_id):
            return 100

    camera = TestCamera(
        TEST_IMAGE_DIR.joinpath(filename),
        calibration_file=get_calibration(camera_name),
    )
    snapshot.assert_match(
        sorted(
            (
                {
                    "id": marker.id,
                    "size": marker.size,
                    "pixel_corners": [
                        coords.to_list() for coords in marker.pixel_corners
                    ],
                    "pixel_centre": marker.pixel_centre.to_list(),
                    "distance": marker.distance,
                    "orientation": tuple(marker.orientation),
                    "spherical": tuple(marker.spherical),
                    "cartesian": marker.cartesian.to_list(),
                }
                for marker in camera.process_frame()
            ),
            key=operator.itemgetter("pixel_centre"),
        )
    )
