import argparse

from zoloto.cameras.camera import Camera
from zoloto.marker_type import ALL_MARKER_TYPES, MarkerType


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=0)
    parser.add_argument(
        "--type",
        type=str,
        default=MarkerType.ARUCO_6X6_250.name,
        choices=ALL_MARKER_TYPES,
    )
    args = parser.parse_args()
    with Camera(args.id, marker_type=MarkerType[args.type], marker_size=100) as camera:
        camera.show(annotate=True)


if __name__ == "__main__":
    main()
