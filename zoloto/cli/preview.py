import argparse

from zoloto.cameras.camera import Camera
from zoloto.marker_type import MarkerType


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=0)
    args = parser.parse_args()
    with Camera(
        args.id, marker_type=MarkerType.ARUCO_6X6_250, marker_size=100
    ) as camera:
        camera.show(annotate=True)


if __name__ == "__main__":
    main()
2
