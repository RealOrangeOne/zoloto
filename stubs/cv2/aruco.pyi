"""
Type stubs for cv2.aruco.
Note that stubs are only written for the parts that we use.
"""
from typing import Iterable, Optional, Tuple

from cv2 import aruco_DetectorParameters, aruco_Dictionary
from numpy import array
from numpy.typing import NDArray

__empty_ndarray = array([])
__default_detector_params = aruco_DetectorParameters()

class CharucoBoard:
    def draw(
        self, outSize: Tuple[int, int], marginSize: int = 0, borderBits: int = 1
    ) -> NDArray: ...

def DetectorParameters_create() -> aruco_DetectorParameters: ...
def estimatePoseSingleMarkers(
    corners: Iterable,
    markerLength: int,
    cameraMatrix: Optional[NDArray],
    distCoeffs: Optional[NDArray],
) -> Tuple[NDArray, NDArray, NDArray]: ...

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
    image: NDArray,
    dictionary: aruco_Dictionary,
    parameters: aruco_DetectorParameters = __default_detector_params,
    cameraMatrix: NDArray = __empty_ndarray,
    distCoeff: NDArray = __empty_ndarray,
) -> Tuple[NDArray, NDArray, NDArray]: ...
def interpolateCornersCharuco(
    markerCorners: NDArray,
    markerIds: NDArray,
    image: NDArray,
    board: CharucoBoard,
    cameraMatrix: NDArray = __empty_ndarray,
    distCoeff: NDArray = __empty_ndarray,
    minMarkers: int = 2,
) -> Tuple[int, NDArray, NDArray]: ...
def calibrateCameraCharuco(
    charucoCorners: Iterable[NDArray],
    charucoIds: Iterable[NDArray],
    board: CharucoBoard,
    imageSize: Tuple[int, int],
    cameraMatrix: Optional[NDArray],
    distCoeff: Optional[NDArray],
) -> Tuple[int, NDArray, NDArray, NDArray, NDArray]: ...
def drawDetectedMarkers(
    image: NDArray,
    corners: NDArray,
    ids: NDArray = __empty_ndarray,
    borderColor: NDArray = __empty_ndarray,
) -> NDArray: ...
def drawMarker(
    dictionary: aruco_Dictionary, markerId: int, sidePixels: int, borderBits: int = 1
) -> NDArray: ...
