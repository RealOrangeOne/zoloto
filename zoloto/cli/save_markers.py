import argparse
from pathlib import Path

from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MARKER_TYPE_NAMES, MarkerType


def main(args: argparse.Namespace) -> None:
    marker_type = MarkerType[args.type]
    output_dir: Path = args.path.resolve()
    output_dir.mkdir(exist_ok=True, parents=True)

    for marker_id in range(marker_type.max_id):
        with MarkerCamera(
            marker_id,
            marker_type=marker_type,
            marker_size=marker_type.min_marker_image_size,
        ) as camera:
            camera.border_size = 1  # HACK: There's validation in the constructor
            print("Saving", marker_id)  # noqa:T001
            camera.save_frame(output_dir / "{}.png".format(marker_id))


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "save-markers", description="Output all marker images for a given type"
    )
    parser.add_argument(
        "type",
        type=str,
        default=MarkerType.ARUCO_6X6.name,
        choices=sorted(MARKER_TYPE_NAMES),
        help="Marker dictionary",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Output directory",
    )
    parser.set_defaults(func=main)
