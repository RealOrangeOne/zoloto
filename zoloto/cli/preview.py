import argparse

import cv2

from zoloto.cameras.camera import Camera


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=0)
    args = parser.parse_args()
    with Camera(args.id, marker_dict=cv2.aruco.DICT_6X6_250) as camera:
        while True:
            frame = camera.capture_frame()
            camera._annotate_frame(frame)
            cv2.imshow("Camera", frame)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()
