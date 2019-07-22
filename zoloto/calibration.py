import json
from pathlib import Path
from typing import NamedTuple

from cv2 import FILE_STORAGE_READ, FILE_STORAGE_WRITE, FileStorage, aruco
from fastcache import clru_cache
from numpy import array

from .marker_dict import MarkerDict

CalibrationParameters = NamedTuple(
    "CalibrationParameters",
    [("camera_matrix", array), ("distance_coefficients", array)],
)

SUPPORTED_EXTENSIONS = ["xml", "json"]


@clru_cache()
def parse_calibration_file(calibration_file: Path) -> CalibrationParameters:
    if not calibration_file.exists():
        raise FileNotFoundError(calibration_file)
    file_extension = calibration_file.suffix
    if file_extension == ".json":
        mtx, dist = json.loads(calibration_file.read_text())
        return CalibrationParameters(array(mtx), array(dist))
    elif file_extension == ".xml":
        storage = FileStorage(str(calibration_file), FILE_STORAGE_READ)
        params = CalibrationParameters(
            storage.getNode("cameraMatrix").mat(), storage.getNode("dist_coeffs").mat()
        )
        storage.release()
        return params
    raise ValueError("Unknown calibration file format: " + file_extension)


def save_calibrations(params: CalibrationParameters, filename: Path):
    file_extension = filename.suffix
    if file_extension == ".json":
        filename.write_text(
            json.dumps(
                [params.camera_matrix.tolist(), params.distance_coefficients.tolist()]
            )
        )
    elif file_extension == ".xml":
        storage = FileStorage(str(filename), FILE_STORAGE_WRITE)
        storage.write("cameraMatrix", params.camera_matrix)
        storage.write("dist_coeffs", params.distance_coefficients)
        storage.release()
    else:
        raise ValueError("Unknown calibration file format: " + file_extension)


@clru_cache()
def get_fake_calibration_parameters(
    size: int, iterations: int = 15
) -> CalibrationParameters:
    """
    HACK: Generate fake calibration parameters
    """
    dictionary = aruco.getPredefinedDictionary(MarkerDict.DICT_6X6_1000)
    seen_corners = []
    seen_ids = []
    image_size = (size, size)
    board = aruco.CharucoBoard_create(6, 6, 0.025, 0.0125, dictionary)
    image = board.draw(image_size)
    for _ in range(iterations):
        corners, ids, _ = aruco.detectMarkers(image, dictionary)
        _, corners, ids = aruco.interpolateCornersCharuco(corners, ids, image, board)
        seen_corners.append(corners)
        seen_ids.append(ids)
    ret, mtx, dist, _, _ = aruco.calibrateCameraCharuco(
        seen_corners, seen_ids, board, image_size, None, None
    )
    return CalibrationParameters(mtx, dist)
