from zoloto.cameras.camera import Camera
from zoloto.marker_dict import MarkerDict


class TestCamera(Camera):
    marker_dict = MarkerDict.DICT_6X6_50

    def get_marker_size(self):
        return 100


camera = TestCamera(0)

while True:
    marker_ids = camera.get_visible_markers()
    print("I can see {} markers".format(len(marker_ids)), end="\r")  # noqa: T001
