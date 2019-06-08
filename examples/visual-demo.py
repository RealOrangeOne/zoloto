"""
This example required `opencv-contrib-python` rather than `opencv-contrib-python-headless`
"""


import datetime

from cv2 import imshow, waitKey
from cv2.aruco import DICT_6X6_50

from yuri.cameras.camera import Camera

camera = Camera(0, marker_dict=DICT_6X6_50)

last_time = datetime.datetime.today().timestamp()
diffs = []

while True:
    frame = camera.capture_frame()
    camera._annotate_frame(frame)
    imshow("demo", frame)
    waitKey(1)

    new_time = datetime.datetime.today().timestamp()
    diffs.append(new_time - last_time)
    last_time = new_time

    if len(diffs) > 10:
        diffs = diffs[-10:]

    print(int(len(diffs) / sum(diffs)), end="\r")
