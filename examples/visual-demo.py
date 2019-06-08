"""
This example required `opencv-contrib-python` rather than `opencv-contrib-python-headless`
"""


from cv2 import imshow, waitKey
from cv2.aruco import DICT_6X6_50

from yuri.cameras.camera import Camera

camera = Camera(0, marker_dict=DICT_6X6_50)


while True:
    frame = camera.capture_frame()
    camera._annotate_frame(frame)
    imshow("demo", frame)
    waitKey(1)
