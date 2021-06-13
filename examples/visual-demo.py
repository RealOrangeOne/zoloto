from chrono import Timer

from zoloto.cameras.camera import Camera
from zoloto.marker_type import MarkerType


class TestCamera(Camera):
    marker_type = MarkerType.DICT_6X6_50

    def get_marker_size(self, marker_id: int) -> int:
        return 100


camera = TestCamera(0)

for frame in camera.iter_show():
    with Timer() as annotate_timer:
        camera._annotate_frame(frame)
    print(round(annotate_timer.elapsed * 1000), end="\r")  # noqa: T001
