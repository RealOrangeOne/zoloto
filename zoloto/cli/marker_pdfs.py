import argparse
from enum import Enum
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


class PageSize(Enum):
    A3 = (297, 420)
    A4 = (210, 297)

    @property
    def pixels(self):
        return (
            mm_to_pixels(self.value[0]),
            mm_to_pixels(self.value[1]),
        )


def main(args: argparse.Namespace) -> None:
    from PIL import Image, ImageOps, ImageDraw

    marker_type = MarkerType[args.type]
    page_size = PageSize[args.page_size]
    output_dir: Path = args.path.resolve()
    output_dir.mkdir(exist_ok=True, parents=True)

    # Captured frame includes white padding, so image size needs to be scaled to account
    pixel_size = args.size // marker_type.min_marker_image_size
    required_size = args.size + (pixel_size * 2)

    if args.size + BORDER_SIZE * 2 > min(page_size.value):
        print(
            f"Warning: Marker size is too large to fit on {args.page_size}"
        )  # noqa:T001

    elif required_size + BORDER_SIZE * 2 > min(page_size.value):
        print(
            f"Warning: Marker size is too large to fit on {args.page_size} with border"
        )  # noqa:T001

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
            resized_image = image.resize([mm_to_pixels(required_size)] * 2, resample=0)

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

            # Put marker onto page
            paper_img = Image.new("RGB", page_size.pixels, (255, 255, 255))
            paper_img.paste(
                bordered_image,
                (
                    (page_size.pixels[0] - img_size) // 2,
                    (page_size.pixels[1] - img_size) // 2,
                ),
            )

            print("Saving", marker_id)  # noqa:T001
            paper_img.save(
                output_dir / "{}.pdf".format(marker_id),
                "PDF",
                quality=100,
                dpi=(DPI, DPI),
            )


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "marker-pdfs", description="Output PDFs for all marker images"
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
    parser.add_argument(
        "--page-size",
        type=str,
        help="Page size. (default: %(default)s)",
        choices=sorted([size.name for size in PageSize]),
        default="A4",
    )
    parser.set_defaults(func=main)
