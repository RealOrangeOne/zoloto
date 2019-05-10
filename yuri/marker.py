from cached_property import cached_property
from cv2 import aruco

from .calibration import CalibrationParameters


class Marker:
    def __init__(
        self, id: int, corners, size, calibration_params: CalibrationParameters
    ):
        self.__id = id
        self.__pixel_corners = corners
        self.__size = size
        self.__camera_calibration_params = calibration_params

    @property
    def id(self):
        return self.__id

    @property
    def size(self):
        return self.__size

    @cached_property
    def __vectors(self):
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
            self.__pixel_corners,
            self.__size,
            self.__camera_calibration_params.camera_matrix,
            self.__camera_calibration_params.distance_coefficients,
        )
        return rvec, tvec

    @cached_property
    def rvec(self):
        rvec, _ = self.__vectors
        return rvec

    @cached_property
    def tvec(self):
        _, tvec = self.__vectors
        return tvec
