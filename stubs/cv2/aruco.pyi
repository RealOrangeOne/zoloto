"""
Type stubs for cv2.aruco.
Note that stubs are only written for the parts that we use.
"""
from typing import Iterable, Optional, Tuple

from cv2 import aruco_DetectorParameters, aruco_Dictionary
from numpy import array, ndarray

__empty_ndarray = array([])
__default_detector_params = aruco_DetectorParameters()

class CharucoBoard:
    def draw(
        self, outSize: Tuple[int, int], marginSize: int = 0, borderBits: int = 1
    ) -> ndarray: ...

def DetectorParameters_create() -> aruco_DetectorParameters: ...
def estimatePoseSingleMarkers(
    corners: Iterable,
    markerLength: int,
    cameraMatrix: Optional[ndarray],
    distCoeffs: Optional[ndarray],
) -> Tuple[ndarray, ndarray, ndarray]: ...

DICT_4X4_1000: int
DICT_5X5_1000: int
DICT_6X6_1000: int
DICT_7X7_1000: int
DICT_ARUCO_ORIGINAL: int
DICT_APRILTAG_16H5: int
DICT_APRILTAG_25H9: int
DICT_APRILTAG_36H10: int
DICT_APRILTAG_36H11: int

def getPredefinedDictionary(dictionary: int) -> aruco_Dictionary: ...
def CharucoBoard_create(
    squaresX: int,
    squaresY: int,
    squareLength: float,
    markerLength: float,
    dictionary: aruco_Dictionary,
) -> CharucoBoard: ...
def detectMarkers(
    image: ndarray,
    dictionary: aruco_Dictionary,
    parameters: aruco_DetectorParameters = __default_detector_params,
    cameraMatrix: ndarray = __empty_ndarray,
    distCoeff: ndarray = __empty_ndarray,
) -> Tuple[ndarray, ndarray, ndarray]: ...
def interpolateCornersCharuco(
    markerCorners: ndarray,
    markerIds: ndarray,
    image: ndarray,
    board: CharucoBoard,
    cameraMatrix: ndarray = __empty_ndarray,
    distCoeff: ndarray = __empty_ndarray,
    minMarkers: int = 2,
) -> Tuple[int, ndarray, ndarray]: ...
def calibrateCameraCharuco(
    charucoCorners: Iterable[ndarray],
    charucoIds: Iterable[ndarray],
    board: CharucoBoard,
    imageSize: Tuple[int, int],
    cameraMatrix: Optional[ndarray],
    distCoeff: Optional[ndarray],
) -> Tuple[int, ndarray, ndarray, ndarray, ndarray]: ...
def drawDetectedMarkers(
    image: ndarray,
    corners: ndarray,
    ids: ndarray = __empty_ndarray,
    borderColor: ndarray = __empty_ndarray,
) -> ndarray: ...
def drawMarker(
    dictionary: aruco_Dictionary, markerId: int, sidePixels: int, borderBits: int = 1
) -> ndarray: ...
