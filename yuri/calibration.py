from functools import lru_cache
from typing import NamedTuple

from cv2 import aruco

CalibrationParameters = NamedTuple(
    "CalibrationParameters", [("camera_matrix", list), ("distance_coefficients", list)]
)


@lru_cache()
def get_fake_calibration_parameters(
    size: int, iterations: int = 15
) -> CalibrationParameters:
    """
    HACK: Generate fake calibration parameters
    """
    assert iterations >= 10
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_1000)
    seen_corners = []
    seen_ids = []
    image_size = (size, size)
    board = aruco.CharucoBoard_create(6, 6, 0.025, 0.0125, dictionary)
    for i in range(iterations):
        image = board.draw(image_size)
        corners, ids, _ = aruco.detectMarkers(image, dictionary)
        _, corners, ids = aruco.interpolateCornersCharuco(corners, ids, image, board)
        seen_corners.append(corners)
        seen_ids.append(ids)
    ret, mtx, dist, _, _ = aruco.calibrateCameraCharuco(
        seen_corners, seen_ids, board, image_size, None, None
    )
    return CalibrationParameters(mtx, dist)
