import pytest
from cv2 import aruco

from zoloto.marker_dict import MarkerDict

EXPECTED_MARKER_DICTS = {
    k.upper() for k, v in aruco.__dict__.items() if k.startswith("DICT_")
}


def test_contains_all_dicts():
    assert {marker.name for marker in MarkerDict} == EXPECTED_MARKER_DICTS


@pytest.mark.parametrize("marker_dict_name", EXPECTED_MARKER_DICTS)
def test_has_correct_marker_ids(marker_dict_name):
    assert (
        getattr(aruco, marker_dict_name) == getattr(MarkerDict, marker_dict_name).value
    )
