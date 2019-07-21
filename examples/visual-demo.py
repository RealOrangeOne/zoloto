from chrono import Timer
from cv2 import imshow, waitKey

from zoloto import assert_has_gui_components
from zoloto.cameras.camera import Camera
from zoloto.marker_dict import MarkerDict

assert_has_gui_components()


class TestCamera(Camera):
    pass


camera = TestCamera(0, marker_dict=MarkerDict.DICT_6X6_50)

while True:
    with Timer() as capture_timer:
        frame = camera.capture_frame()
    with Timer() as annotate_timer:
        camera._annotate_frame(frame)
    imshow("demo", frame)
    waitKey(1)
    print(  # noqa: T001
        round(capture_timer.elapsed * 1000),
        round(annotate_timer.elapsed * 1000),
        end="\r",
    )
