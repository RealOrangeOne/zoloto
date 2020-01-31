from chrono import Timer
from numpy import ndarray

from zoloto.cameras.camera import Camera
from zoloto.marker_type import MarkerType
from zoloto.viewer import CameraViewer


class TestCamera(Camera):
    marker_type = MarkerType.DICT_6X6_50

    def get_marker_size(self, marker_id: int) -> int:
        return 100


class Viewer(CameraViewer):
    def on_frame(self, frame: ndarray) -> ndarray:
        with Timer() as annotate_timer:
            camera._annotate_frame(frame)
        print(round(annotate_timer.elapsed * 1000), end="\r")  # noqa: T001
        return frame


camera = TestCamera(0)


Viewer(camera).start()
