from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

from cv2 import FILE_STORAGE_READ, FILE_STORAGE_WRITE, FileStorage, aruco
from numpy import ndarray

from .marker_type import MarkerType


class CalibrationParameters(NamedTuple):
    camera_matrix: ndarray
    distance_coefficients: ndarray


@lru_cache()
def parse_calibration_file(calibration_file: Path) -> CalibrationParameters:
    if not calibration_file.exists():
        raise FileNotFoundError(calibration_file)
    storage = FileStorage(str(calibration_file), FILE_STORAGE_READ)
    params = CalibrationParameters(
        storage.getNode("cameraMatrix").mat(),
        storage.getNode("dist_coeffs").mat(),
    )
    storage.release()
    return params


def save_calibrations(params: CalibrationParameters, filename: Path) -> None:
    storage = FileStorage(str(filename), FILE_STORAGE_WRITE)
    storage.write("cameraMatrix", params.camera_matrix)
    storage.write("dist_coeffs", params.distance_coefficients)
    storage.release()


@lru_cache()
def get_fake_calibration_parameters() -> CalibrationParameters:
    """
    HACK: Generate fake calibration parameters
    """

    dictionary = aruco.getPredefinedDictionary(MarkerType.ARUCO_6X6)
    seen_corners = []
    seen_ids = []
    image_size = (200, 200)
    board = aruco.CharucoBoard_create(6, 6, 0.025, 0.0125, dictionary)
    image = board.draw(image_size)
    for _ in range(15):
        corners, ids, _ = aruco.detectMarkers(image, dictionary)
        _, corners, ids = aruco.interpolateCornersCharuco(corners, ids, image, board)
        seen_corners.append(corners)
        seen_ids.append(ids)
    ret, mtx, dist, _, _ = aruco.calibrateCameraCharuco(
        seen_corners, seen_ids, board, image_size, None, None
    )
    return CalibrationParameters(mtx, dist)
