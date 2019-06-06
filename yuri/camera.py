from itertools import groupby
from typing import Tuple

import cv2

from .calibration import get_fake_calibration_parameters, parse_calibration_file
from .marker import Marker


class BaseCamera:
    def __init__(self, **kwargs):
        self.marker_dictionary = cv2.aruco.getPredefinedDictionary(
            kwargs["marker_dict"]
        )
        self.calibration_file = kwargs.get("calibration_file")
        self.detector_params = self.get_detector_params(
            cv2.aruco.DetectorParameters_create()
        )

    def get_calibrations(self):
        if self.calibration_file is None:
            raise FileNotFoundError("Missing calibration file")
        return parse_calibration_file(self.calibration_file)

    def get_resolution(self) -> Tuple[int, int]:
        # TODO: Implement everywhere else
        raise NotImplementedError()

    def get_detector_params(self, params):
        return params

    def get_marker_size(self, marker_id: int) -> int:
        raise NotImplementedError()

    def capture_frame(self):
        raise NotImplementedError()

    def save_frame(self, filename, annotate=False, frame=None):
        if frame is None:
            frame = self.capture_frame()
        if annotate:
            ids, corners = self._get_ids_and_corners(frame)
            cv2.aruco.drawDetectedMarkers(frame, [corners], ids)
        cv2.imwrite(filename, frame)
        return frame

    def _get_ids_and_corners(self, frame=None):
        if frame is None:
            frame = self.capture_frame()
        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, self.marker_dictionary, parameters=self.detector_params
        )
        if ids is None:
            return [], []
        return ids[0], corners[0]

    def process_frame(self, frame=None):
        ids, corners = self._get_ids_and_corners(frame)
        calibration_params = self.get_calibrations()
        for corners, id in zip(corners, ids):
            yield Marker(id, corners, self.get_marker_size(id), calibration_params)

    def process_frame_eager(self, frame=None):
        ids, corners = self._get_ids_and_corners(frame)
        calibration_params = self.get_calibrations()

        def get_marker_size(id_and_corners):
            return self.get_marker_size(id_and_corners[0])

        sorted_corners = sorted(zip(ids, corners), key=get_marker_size)
        for size, ids_and_corners in groupby(sorted_corners, get_marker_size):
            ids, corners = zip(*ids_and_corners)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, size, *calibration_params
            )
            for id, corners, rvec, tvec in zip(ids, corners, rvecs[0], tvecs[0]):
                yield Marker(id, corners, size, calibration_params, (rvec, tvec))

    def get_visible_markers(self, frame=None):
        ids, _ = self._get_ids_and_corners(frame)
        return ids

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if tb:
            return False

        self.close()

    def __del__(self):
        self.close()


class FileCamera(BaseCamera):
    def __init__(self, image_path, **kwargs):
        self.image_path = image_path
        super().__init__(**kwargs)

    def capture_frame(self):
        return cv2.imread(self.image_path)


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


class SnapshotCamera(BaseCamera):
    """
    A modified version of Camera optimised for single use.

    - Doesn't keep the camera open between captures
    """

    def __init__(self, camera_id, **kwargs):
        super().__init__(**kwargs)
        self.camera_id = camera_id

    def _create_video_capture(self):
        return cv2.VideoCapture(self.camera_id)

    def capture_frame(self):
        video_capture = self._create_video_capture()
        _, frame = video_capture.read()
        video_capture.release()
        return frame


class MarkerCamera(BaseCamera):
    """
    A camera which always returns a single, full-screen marker
    """

    BORDER_SIZE = 40

    def __init__(self, marker_id, **kwargs):
        super().__init__(**kwargs)
        self.marker_id = marker_id
        self.marker_size = kwargs["marker_size"]

    def get_marker_size(self, marker_id: int):
        return self.marker_size

    def get_calibrations(self):
        return get_fake_calibration_parameters(self.marker_size)

    def get_resolution(self) -> Tuple[int, int]:
        size = int(self.get_marker_size(self.marker_id) + self.BORDER_SIZE * 2)
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
