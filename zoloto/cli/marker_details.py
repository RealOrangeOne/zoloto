import argparse

from zoloto.marker_type import MarkerType

ATTRIBUTES_TO_DISPLAY = [
    "marker_count",
    "max_id",
    "min_marker_image_size",
    "marker_size",
]


def main(args: argparse.Namespace) -> None:
    for marker_type in MarkerType:
        print("Type", marker_type.name)  # noqa:T001

        for attr in ATTRIBUTES_TO_DISPLAY:
            print(  # noqa:T001
                "\t",
                getattr(MarkerType, attr).__doc__.strip() + ":",
                getattr(marker_type, attr),
            )


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "marker-details", description="Show some details about the marker types"
    )
    parser.set_defaults(func=main)
