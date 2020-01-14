from chrono import Timer

from zoloto.cameras.camera import Camera
from zoloto.marker_dict import MarkerDict
from zoloto.viewer import CameraViewer


class TestCamera(Camera):
    pass


class Viewer(CameraViewer):
    def on_frame(self, frame):
        with Timer() as annotate_timer:
            frame = camera._annotate_frame(frame)
        print(round(annotate_timer.elapsed * 1000), end="\r")  # noqa: T001
        return frame


camera = TestCamera(0, marker_dict=MarkerDict.DICT_6X6_50)


Viewer(camera).start()
