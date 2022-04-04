import argparse
from pathlib import Path

from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MARKER_TYPE_NAMES, MarkerType
from zoloto.utils import parse_ranges


def main(args: argparse.Namespace) -> None:
    from PIL import Image, ImageDraw

    marker_type = MarkerType[args.type]
    output_dir: Path = args.path.resolve()
    output_dir.mkdir(exist_ok=True, parents=True)

    marker_ids = (
        parse_ranges(args.range) if args.range != "ALL" else marker_type.marker_ids
    )

    for marker_id in sorted(marker_ids):
        with MarkerCamera(
            marker_id,
            marker_type=marker_type,
            marker_size=marker_type.min_marker_image_size,
        ) as camera:
            camera.border_size = 1  # HACK: There's validation in the constructor
            print("Saving", marker_id)  # noqa:T001

            if args.raw:
                camera.save_frame(output_dir / "{}.png".format(marker_id))
            else:
                image = Image.fromarray(camera.capture_frame())

                # Resize the image to the required size
                resized_image = image.resize((500, 500), resample=0)

                img_size = resized_image.size[0]

                ImageDraw.Draw(resized_image).text(
                    (25, img_size - 25),
                    args.description_format.format(
                        marker_type=marker_type.name, marker_id=marker_id
                    ),
                    anchor="lt",
                )
                resized_image.save(output_dir / "{}.png".format(marker_id))


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
    parser.add_argument(
        "--raw",
        help="Remove the additional annotations around the marker, such that it's just the pure marker",
        action="store_true",
    )
    parser.add_argument(
        "--description-format",
        type=str,
        help="Text format for the description on the marker images. `marker_id` and `marker_type` are available for string format replacement. (default: %(default)s)",
        default="{marker_type} {marker_id}",
    )
    parser.add_argument(
        "--range",
        help="Marker ids to output (inclusive)",
        default="ALL",
    )
    parser.set_defaults(func=main)
