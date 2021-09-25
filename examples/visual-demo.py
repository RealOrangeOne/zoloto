from zoloto.cameras.camera import Camera
from zoloto.marker_type import MarkerType

camera = Camera(0, marker_type=MarkerType.DICT_6X6_50, marker_size=100)

camera.show(annotate=True)
