from enum import IntEnum

from cv2 import aruco


class MarkerType(IntEnum):
    ARUCO_4X4_50 = aruco.DICT_4X4_50
    ARUCO_4X4_100 = aruco.DICT_4X4_100
    ARUCO_4X4_250 = aruco.DICT_4X4_250
    ARUCO_4X4_1000 = aruco.DICT_4X4_1000
    ARUCO_5X5_50 = aruco.DICT_5X5_50
    ARUCO_5X5_100 = aruco.DICT_5X5_100
    ARUCO_5X5_250 = aruco.DICT_5X5_250
    ARUCO_5X5_1000 = aruco.DICT_5X5_1000
    ARUCO_6X6_50 = aruco.DICT_6X6_50
    ARUCO_6X6_100 = aruco.DICT_6X6_100
    ARUCO_6X6_250 = aruco.DICT_6X6_250
    ARUCO_6X6_1000 = aruco.DICT_6X6_1000
    ARUCO_7X7_50 = aruco.DICT_7X7_50
    ARUCO_7X7_100 = aruco.DICT_7X7_100
    ARUCO_7X7_250 = aruco.DICT_7X7_250
    ARUCO_7X7_1000 = aruco.DICT_7X7_1000
    ARUCO_ORIGINAL = aruco.DICT_ARUCO_ORIGINAL
    APRILTAG_16H5 = aruco.DICT_APRILTAG_16H5
    APRILTAG_25H9 = aruco.DICT_APRILTAG_25H9
    APRILTAG_36H10 = aruco.DICT_APRILTAG_36H10
    APRILTAG_36H11 = aruco.DICT_APRILTAG_36H11


# Non-overlapping marker types
MARKER_TYPES = frozenset(
    {
        MarkerType.ARUCO_4X4_1000,
        MarkerType.ARUCO_5X5_1000,
        MarkerType.ARUCO_6X6_1000,
        MarkerType.ARUCO_7X7_1000,
        MarkerType.ARUCO_ORIGINAL,
        MarkerType.APRILTAG_16H5,
        MarkerType.APRILTAG_25H9,
        MarkerType.APRILTAG_36H10,
        MarkerType.APRILTAG_36H11,
    }
)


MARKER_TYPE_NAMES = frozenset(m.name for m in MARKER_TYPES)
