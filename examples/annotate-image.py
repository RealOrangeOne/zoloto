import sys
from pathlib import Path

from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_type import MarkerType

with ImageFileCamera(
    Path(sys.argv[1]), marker_type=MarkerType.DICT_6X6_50, marker_size=100
) as camera:
    camera.save_frame(Path(sys.argv[2]), annotate=True)
    print(  # noqa: T001
        "Saw {} markers in this image".format(len(camera.get_visible_markers()))
    )
