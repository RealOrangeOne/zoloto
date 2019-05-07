from cached_property import cached_property
from cv2 import aruco

from .calibration import CalibrationParameters


class Marker:
    def __init__(
        self, id: int, corners, size, calibration_params: CalibrationParameters
    ):
        self.id = id
        self.pixel_corners = corners
        self.size = size
        self._camera_calibration_params = calibration_params

    @cached_property
    def _vectors(self):
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
            self.pixel_corners,
            self.size,
            self._camera_calibration_params.camera_matrix,
            self._camera_calibration_params.distance_coefficients,
        )
        return rvec, tvec

    @cached_property
    def rvec(self):
        rvec, _ = self._vectors
        return rvec

    @cached_property
    def tvec(self):
        _, tvec = self._vectors
        return tvec
