import cv2
import pytest

from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MarkerType


@pytest.mark.parametrize("marker_type", MarkerType)
def test_marker_type_max_id_allowed(marker_type: MarkerType) -> None:
    camera = MarkerCamera(marker_type.max_id, marker_size=100, marker_type=marker_type)
    assert camera.get_visible_markers() == [marker_type.max_id]


@pytest.mark.parametrize("marker_type", MarkerType)
def test_marker_type_max_id_disallowed(marker_type: MarkerType) -> None:
    camera = MarkerCamera(
        marker_type.max_id + 1, marker_size=100, marker_type=marker_type
    )
    with pytest.raises(cv2.error):
        camera.get_visible_markers()
