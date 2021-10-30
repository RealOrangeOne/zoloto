import argparse
from pathlib import Path

from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MARKER_TYPE_NAMES, MarkerType
from zoloto.utils import parse_ranges

DPI = 72
BORDER_SIZE = 2


def mm_to_inches(mm: int) -> float:
    """
    Convert millimeters to inches
    """
    inches = mm * 0.0393701
    inches = round(inches, 4)
    return inches


def mm_to_pixels(mm: int) -> int:
    return int(mm_to_inches(mm) * DPI)


A4 = (mm_to_pixels(210), mm_to_pixels(297))


def main(args: argparse.Namespace) -> None:
    from PIL import Image, ImageOps, ImageDraw

    marker_type = MarkerType[args.type]
    output_dir: Path = args.path.resolve()
    output_dir.mkdir(exist_ok=True, parents=True)

    if args.size + BORDER_SIZE * 2 > 210:
        print("Warning: Marker size is too large to fit on A4")  # noqa:T001

    marker_ids = (
        parse_ranges(args.range) if args.range != "ALL" else range(marker_type.max_id)
    )

    for marker_id in sorted(marker_ids):
        with MarkerCamera(
            marker_id,
            marker_type=marker_type,
            marker_size=marker_type.min_marker_image_size,
        ) as camera:
            camera.border_size = 1  # HACK: There's validation in the constructor
            image = Image.fromarray(camera.capture_frame())

            # Resize the image to the required size
            resized_image = image.resize([mm_to_pixels(args.size)] * 2, resample=0)

            # Add a border to the marker, which includes padding
            bordered_image = ImageOps.expand(
                resized_image, border=BORDER_SIZE, fill="grey"
            )
            img_size = bordered_image.size[0]

            ImageDraw.Draw(bordered_image).text(
                (25, img_size - 25),
                args.description_format.format(
                    marker_type=marker_type.name, marker_id=marker_id
                ),
                anchor="lt",
            )

            # Put marker onto A4 page
            a4_img = Image.new("RGB", A4, (255, 255, 255))
            a4_img.paste(
                bordered_image, ((A4[0] - img_size) // 2, (A4[1] - img_size) // 2)
            )

            print("Saving", marker_id)  # noqa:T001
            a4_img.save(
                output_dir / "{}.pdf".format(marker_id),
                "PDF",
                quality=100,
                dpi=(DPI, DPI),
            )


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "marker-pdfs", description="Output A4 PDFs for all marker images"
    )
    parser.add_argument(
        "type",
        type=str,
        choices=sorted(MARKER_TYPE_NAMES),
        help="Marker dictionary",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Output directory",
    )
    parser.add_argument(
        "size",
        type=float,
        help="Size of marker (mm)",
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
