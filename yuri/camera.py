import os

import cv2

MARKER_SIZE_MM = 100


class BaseCamera:
    def __init__(self, **kwargs):
        self.marker_size = kwargs.get("marker_size", MARKER_SIZE_MM)
        self.marker_dictionary = cv2.aruco.getPredefinedDictionary(
            kwargs["marker_dict"]
        )

    def capture_frame(self):
        raise NotImplementedError()

    def save_frame(self, filename, frame=None):
        if frame is None:
            frame = self.capture_frame()
        cv2.imwrite(filename, frame)
        return frame

    def close(self):
        pass


class ImageFileCamera(BaseCamera):
    def __init__(self, image_path, **kwargs):
        self.image = None
        assert os.path.exists(image_path)
        self.image_path = image_path
        super().__init__(self)

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

    def __init__(self, marker_id, **kwargs):
        super().__init__(**kwargs)
        self.marker_id = marker_id

    def capture_frame(self):
        return cv2.aruco.drawMarker(
            self.marker_dictionary, self.marker_id, self.marker_size
        )
