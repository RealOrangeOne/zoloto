from cv2 import aruco

from yuri.camera import Camera

camera = Camera(0, marker_dict=aruco.DICT_6X6_50)

while True:
    marker_ids = camera.get_visible_markers()
    print("I can see {} markers".format(len(marker_ids)), end="\r")  # noqa: F401
