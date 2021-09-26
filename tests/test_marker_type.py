import pytest
from cv2 import aruco

from zoloto.marker_type import MarkerType

EXPECTED_MARKER_TYPES = {
    k.upper() for k in aruco.__dict__.keys() if k.startswith("DICT_")
}


@pytest.mark.parametrize("marker_type_name", EXPECTED_MARKER_TYPES)
def test_has_all_marker_dicts(marker_type_name: str) -> None:
    MarkerType(getattr(aruco, marker_type_name))


@pytest.mark.parametrize("marker_type_name", EXPECTED_MARKER_TYPES)
def test_correct_marker_dict(marker_type_name: str) -> None:
    marker_type_zoloto = marker_type_name.lstrip("DICT_")
    if not marker_type_zoloto.startswith(("APRILTAG", "ARUCO")):
        marker_type_zoloto = "ARUCO_" + marker_type_zoloto

    marker_type = MarkerType[marker_type_zoloto]
    assert marker_type.value == getattr(aruco, marker_type_name)
