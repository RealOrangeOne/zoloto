import argparse

from zoloto.cameras.camera import Camera
from zoloto.marker_type import MARKER_TYPE_NAMES, MarkerType


def main(args: argparse.Namespace) -> None:
    with Camera(args.id, marker_type=MarkerType[args.type], marker_size=100) as camera:
        print("Starting preview... Press 'q' to exit.")  # noqa: T001
        camera.show(annotate=True)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "preview", description="Preview webcam feed with annotated markers"
    )
    parser.add_argument(
        "--id", type=int, default=0, help="Camera ID to use (default: %(default)s)"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=sorted(MARKER_TYPE_NAMES),
        help="Marker dictionary",
    )
    parser.set_defaults(func=main)
