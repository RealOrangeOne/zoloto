from enum import IntEnum

from cv2 import aruco, aruco_Dictionary


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
    def dictionary(self) -> aruco_Dictionary:
        """
        The underlying OpenCV marker dictionary
        """
        return aruco.getPredefinedDictionary(self.value)

    @property
    def marker_count(self) -> int:
        """
        The total number of markers available
        """
        return len(self.dictionary.bytesList)

    @property
    def max_id(self) -> int:
        """
        The highest id available
        """
        return self.marker_count - 1

    @property
    def min_marker_image_size(self) -> int:
        """
        Minimum size of a marker in pixels
        """
        return self.marker_size + 2

    @property
    def marker_size(self) -> int:
        """
        Number of bits along 1 size of a marker
        """
        return self.dictionary.markerSize


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

MAX_ALL_ALLOWED_ID = min(m.max_id for m in MarkerType)
