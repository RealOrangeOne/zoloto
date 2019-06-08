import sys

from cv2 import aruco

from yuri.cameras.file import ImageFileCamera

with ImageFileCamera(sys.argv[1], marker_dict=aruco.DICT_6X6_50) as camera:
    camera.save_frame(sys.argv[2], annotate=True)
    print(  # noqa: T001
        "Saw {} markers in this image".format(len(camera.get_visible_markers()))
    )
