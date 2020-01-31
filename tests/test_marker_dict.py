import pytest
from cv2 import aruco

from zoloto.marker_type import MarkerType

EXPECTED_marker_typeS = {
    k.upper() for k, v in aruco.__dict__.items() if k.startswith("DICT_")
}


def test_contains_all_dicts() -> None:
    assert {marker.name for marker in MarkerType} == EXPECTED_marker_typeS


@pytest.mark.parametrize("marker_type_name", EXPECTED_marker_typeS)
def test_has_correct_marker_ids(marker_type_name: str) -> None:
    assert (
        getattr(aruco, marker_type_name) == getattr(MarkerType, marker_type_name).value
    )
