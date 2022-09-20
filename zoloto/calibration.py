from functools import lru_cache
from pathlib import Path
from typing import NamedTuple, Tuple

from cv2 import FILE_STORAGE_READ, FileStorage, aruco
from numpy import floating
from numpy.typing import NDArray

from .marker_type import MarkerType


class CalibrationParameters(NamedTuple):
    camera_matrix: NDArray[floating]
    distance_coefficients: NDArray[floating]
    resolution: Tuple[int, int]


def parse_calibration_file(calibration_file: Path) -> CalibrationParameters:
    if not calibration_file.exists():
        raise FileNotFoundError(calibration_file)
    storage = FileStorage(str(calibration_file), FILE_STORAGE_READ)
    resolution_node = storage.getNode("cameraResolution")
    params = CalibrationParameters(
        storage.getNode("cameraMatrix").mat(),
        storage.getNode("dist_coeffs").mat(),
        (
            int(resolution_node.at(0).real()),
            int(resolution_node.at(1).real()),
        ),
    )
    storage.release()
    return params


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
    return CalibrationParameters(mtx, dist, (1280, 720))
