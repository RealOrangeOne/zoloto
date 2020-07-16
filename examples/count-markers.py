from zoloto.cameras.camera import Camera
from zoloto.marker_type import MarkerType

camera = Camera(0, marker_type=MarkerType.DICT_6X6_50, marker_size=100)

while True:
    marker_ids = camera.get_visible_markers()
    print("I can see {} markers".format(len(marker_ids)), end="\r")  # noqa: T001
