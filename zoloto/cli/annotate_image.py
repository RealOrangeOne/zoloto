import argparse
from pathlib import Path

from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_type import MARKER_TYPE_NAMES, MarkerType


def main(args: argparse.Namespace) -> None:
    with ImageFileCamera(
        Path(args.in_file), marker_type=MarkerType[args.type], marker_size=100
    ) as camera:
        camera.save_frame(Path(args.out_file), annotate=True)

        print(  # noqa: T001
            "Saw {} markers in this image".format(len(camera.get_visible_markers()))
        )


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("annotate-image", description="Annotate an image")
    parser.add_argument("in_file", type=str, help="")
    parser.add_argument("out_file", type=str, help="")
    parser.add_argument(
        "--type",
        type=str,
        default=MarkerType.ARUCO_6X6.name,
        choices=sorted(MARKER_TYPE_NAMES),
        help="Marker dictionary",
    )
    parser.set_defaults(func=main)
