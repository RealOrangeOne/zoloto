from itertools import groupby

import cv2

from yuri.calibration import parse_calibration_file
from yuri.marker import Marker


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
