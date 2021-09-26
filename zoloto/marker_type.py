from enum import IntEnum

from cv2 import aruco


class MarkerType(IntEnum):
    ARUCO_4X4 = aruco.DICT_4X4_1000
    ARUCO_5X5 = aruco.DICT_5X5_1000
    ARUCO_6X6 = aruco.DICT_6X6_1000
    ARUCO_7X7 = aruco.DICT_7X7_1000
    ARUCO_ORIGINAL = aruco.DICT_ARUCO_ORIGINAL
    APRILTAG_16H5 = aruco.DICT_APRILTAG_16H5
    APRILTAG_25H9 = aruco.DICT_APRILTAG_25H9
    APRILTAG_36H10 = aruco.DICT_APRILTAG_36H10
    APRILTAG_36H11 = aruco.DICT_APRILTAG_36H11

    @property
    def dictionary_size(self) -> int:
        """
        The total number of markers available
        """
        return len(aruco.getPredefinedDictionary(self.value).bytesList)

    @property
    def max_id(self) -> int:
        """
        The highest id available
        """
        return self.dictionary_size - 1


# Non-overlapping marker types
MARKER_TYPES = frozenset(
    {
        MarkerType.ARUCO_4X4,
        MarkerType.ARUCO_5X5,
        MarkerType.ARUCO_6X6,
        MarkerType.ARUCO_7X7,
        MarkerType.ARUCO_ORIGINAL,
        MarkerType.APRILTAG_16H5,
        MarkerType.APRILTAG_25H9,
        MarkerType.APRILTAG_36H10,
        MarkerType.APRILTAG_36H11,
    }
)


MARKER_TYPE_NAMES = frozenset(m.name for m in MARKER_TYPES)
