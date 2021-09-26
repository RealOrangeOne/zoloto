import cv2
import pytest

from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MAX_ALL_ALLOWED_ID, MarkerType


@pytest.mark.parametrize("marker_type", MarkerType)
def test_marker_type_max_id_allowed(marker_type: MarkerType) -> None:
    camera = MarkerCamera(marker_type.max_id, marker_size=100, marker_type=marker_type)
    assert camera.get_visible_markers() == [marker_type.max_id]


@pytest.mark.parametrize("marker_type", MarkerType)
def test_marker_type_max_id_disallowed(marker_type: MarkerType) -> None:
    camera = MarkerCamera(marker_type.max_id, marker_size=100, marker_type=marker_type)
    camera.marker_id = marker_type.max_id + 1  # There's an assertion in the constructor
    with pytest.raises(cv2.error):
        camera.get_visible_markers()


def test_max_all_allowed_id() -> None:
    for marker_type in MarkerType:
        assert marker_type.max_id >= MAX_ALL_ALLOWED_ID
