import sys
from pathlib import Path

from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_dict import MarkerDict


class TestCamera(ImageFileCamera):
    marker_dict = MarkerDict.DICT_6X6_50


with TestCamera(Path(sys.argv[1])) as camera:
    camera.save_frame(sys.argv[2], annotate=True)
    print(  # noqa: T001
        "Saw {} markers in this image".format(len(camera.get_visible_markers()))
    )
