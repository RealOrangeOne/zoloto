import argparse
from pathlib import Path

from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_type import MarkerType


def main(args: argparse.Namespace) -> None:
    for marker_type in MarkerType:
        with ImageFileCamera(
            Path(args.file), marker_type=marker_type, marker_size=100
        ) as camera:
            visible_markers = camera.get_visible_markers()

            if visible_markers:
                print(  # noqa: T001
                    "Found", len(visible_markers), marker_type.name, "tokens"
                )


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "count-markers", description="Count markers in an image"
    )
    parser.add_argument("file", type=str, help="")
    parser.set_defaults(func=main)
