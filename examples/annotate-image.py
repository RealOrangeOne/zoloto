import sys

from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_dict import MarkerDict

with ImageFileCamera(sys.argv[1], marker_dict=MarkerDict.DICT_6X6_50) as camera:
    camera.save_frame(sys.argv[2], annotate=True)
    print(  # noqa: T001
        "Saw {} markers in this image".format(len(camera.get_visible_markers()))
    )
