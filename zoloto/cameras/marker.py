from typing import Tuple

import cv2
from numpy.typing import NDArray

from zoloto.calibration import get_fake_calibration_parameters
from zoloto.marker_type import MarkerType

from .base import BaseCamera


class MarkerCamera(BaseCamera):
    """
    A camera which always returns a single, full-screen marker
    """

    MIN_BORDER_SIZE = 3

    def __init__(
        self,
        marker_id: int,
        marker_size: int,
        *,
        marker_type: MarkerType,
        border_size: int = 40,
    ) -> None:

        if marker_id > marker_type.max_id:
            raise ValueError(
                "marker id {} must be less than the maximum allowed by {}: {}".format(
                    marker_id, marker_type.name, marker_type.max_id
                )
            )

        if marker_size < marker_type.min_marker_image_size:
            raise ValueError(
                "marker must be at least {} pixels wide".format(
                    marker_type.min_marker_image_size
                )
            )

        if border_size < self.MIN_BORDER_SIZE:
            raise ValueError(
                "Border size must be at least {}".format(self.MIN_BORDER_SIZE)
            )

        super().__init__(
            marker_size=marker_size,
            marker_type=marker_type,
        )
        self.marker_id = marker_id
        self.border_size = border_size
        self.calibration_params = get_fake_calibration_parameters()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.marker_id} size={self._marker_size} type={self.marker_type.name}>"

    def get_resolution(self) -> Tuple[int, int]:
        size = int(self.get_marker_size(self.marker_id) + self.border_size * 2)
        return size, size

    def capture_frame(self) -> NDArray:
        image = cv2.aruco.drawMarker(
            self.marker_dictionary, self.marker_id, self.get_marker_size(self.marker_id)
        )
        return cv2.copyMakeBorder(
            image,
            self.border_size,
            self.border_size,
            self.border_size,
            self.border_size,
            cv2.BORDER_CONSTANT,
            value=[255, 0, 0],
        )
