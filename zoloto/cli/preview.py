import argparse

from zoloto.cameras.camera import Camera
from zoloto.marker_dict import MarkerDict
from zoloto.viewer import CameraViewer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=0)
    args = parser.parse_args()
    with Camera(args.id, marker_dict=MarkerDict.DICT_6X6_250) as camera:
        CameraViewer(camera, annotate=True).start()


if __name__ == "__main__":
    main()
