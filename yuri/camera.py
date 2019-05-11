import os
from typing import Tuple

import cv2

from .calibration import get_fake_calibration_parameters, parse_calibration_file
from .marker import Marker


class BaseCamera:
    def __init__(self, **kwargs):
        self.marker_size = kwargs.get("marker_size")
        self.marker_dictionary = cv2.aruco.getPredefinedDictionary(
            kwargs["marker_dict"]
        )
        self.calibration_file = kwargs.get("calibration_file")

    def get_calibrations(self):
        if self.calibration_file is None:
            raise FileNotFoundError("Missing calibration file")
        return parse_calibration_file(self.calibration_file)

    def get_resolution(self) -> Tuple[int, int]:
        # TODO: Implement everywhere else
        raise NotImplementedError()

    def get_marker_size(self, marker_id: int) -> int:
        if self.marker_size is not None:
            return self.marker_size
        raise ValueError("Can't get marker size for marker {}".format(marker_id))

    def capture_frame(self):
        raise NotImplementedError()

    def save_frame(self, filename, frame=None):
        if frame is None:
            frame = self.capture_frame()
        cv2.imwrite(filename, frame)
        return frame

    def process_frame(self, frame=None):
        if frame is None:
            frame = self.capture_frame()
        corners, ids, _ = cv2.aruco.detectMarkers(frame, self.marker_dictionary)
        if not corners or not ids:
            return []
        corners = corners[0]
        ids = ids[0]
        calibration_params = self.get_calibrations()
        return [
            Marker(id, corners, self.get_marker_size(id), calibration_params)
            for corners, id in zip(corners, ids)
        ]

    def close(self):
        pass


class FileCamera(BaseCamera):
    def __init__(self, image_path, **kwargs):
        self.image = None
        assert os.path.exists(image_path)
        self.image_path = image_path
        super().__init__(**kwargs)

    def capture_frame(self):
        if self.image is None:
            self.image = cv2.imread(self.image_path)
        return self.image

    def close(self):
        super().close()
        if self.image is not None:
            self.image.release()


class Camera(BaseCamera):
    def __init__(self, camera_id, **kwargs):
        super().__init__(**kwargs)
        self.camera_id = camera_id
        self.video_capture = self._create_video_capture()

    def _create_video_capture(self):
        return cv2.VideoCapture(self.camera_id)

    def capture_frame(self):
        _, frame = self.video_capture.read()
        return frame

    def close(self):
        super().close()
        self.video_capture.release()


class SnapshotCamera(Camera):
    """
    A modified version of Camera optimised for singe use.

    - Doesn't keep the camera open between captures
    """

    def capture_frame(self):
        frame = super().capture_frame()
        self.video_capture.release()  # explicitly release the previos video capture
        self.video_capture = self._create_video_capture()
        return frame


class MarkerCamera(BaseCamera):
    """
    A camera which always returns a single full-screen marker
    """

    BORDER_SIZE = 40

    def __init__(self, marker_id, **kwargs):
        super().__init__(**kwargs)
        self.marker_id = marker_id

    def get_calibrations(self):
        return get_fake_calibration_parameters(self.marker_size)

    def get_resolution(self) -> Tuple[int, int]:
        size = int(self.marker_size + self.BORDER_SIZE * 2)
        return size, size

    def capture_frame(self):
        image = cv2.aruco.drawMarker(
            self.marker_dictionary, self.marker_id, self.marker_size
        )
        return cv2.copyMakeBorder(
            image,
            self.BORDER_SIZE,
            self.BORDER_SIZE,
            self.BORDER_SIZE,
            self.BORDER_SIZE,
            cv2.BORDER_CONSTANT,
            value=[255, 0, 0],
        )
