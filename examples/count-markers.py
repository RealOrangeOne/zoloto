from zoloto.cameras.camera import Camera
from zoloto.marker_type import MarkerType


class TestCamera(Camera):
    def get_marker_size(self, marker_id: int) -> int:
        return 100


camera = TestCamera(0, marker_type=MarkerType.DICT_6X6_50)

while True:
    marker_ids = camera.get_visible_markers()
    print("I can see {} markers".format(len(marker_ids)), end="\r")  # noqa: T001
