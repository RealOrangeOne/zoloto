"""
Type stubs for cv2.aruco.
Note that stubs are only written for the parts that we use.
"""
from typing import Iterable, Optional, Tuple

from cv2 import aruco_DetectorParameters
from numpy import ndarray


def DetectorParameters_create() -> aruco_DetectorParameters:
    ...


def estimatePoseSingleMarkers(
    corners: Iterable,
    markerLength: int,
    cameraMatrix: Optional[ndarray],
    distCoeffs: Optional[ndarray],
) -> Tuple[ndarray, ndarray, ndarray]:
    ...
