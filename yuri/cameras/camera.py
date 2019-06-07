from cv2 import VideoCapture

from .base import BaseCamera


class Camera(BaseCamera):
    def __init__(self, camera_id: int, **kwargs):
        super().__init__(**kwargs)
        self.video_capture = VideoCapture(camera_id)

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

    def __init__(self, camera_id: int, **kwargs):
        super().__init__(**kwargs)
        self.camera_id = camera_id

    def capture_frame(self):
        video_capture = VideoCapture(self.camera_id)
        _, frame = video_capture.read()
        video_capture.release()
        return frame
