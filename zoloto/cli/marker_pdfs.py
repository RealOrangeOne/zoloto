from __future__ import annotations

import argparse
from enum import Enum
from pathlib import Path

from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MARKER_TYPE_NAMES, MarkerType
from zoloto.utils import parse_ranges

DPI = 72
BORDER_FILL = "lightgrey"


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
    def pixels(self) -> tuple[int, int]:
        return (
            mm_to_pixels(self.value[0]),
            mm_to_pixels(self.value[1]),
        )


def main(args: argparse.Namespace) -> None:
    from PIL import Image, ImageDraw, ImageOps

    marker_type = MarkerType[args.type]
    page_size = PageSize[args.page_size]

    if args.force_a4 and page_size == PageSize.A4:
        # NOTE: This also currently only supports A3 (halving the image)
        print("--force-a4 doesn't make sense with a page size of A4")  # noqa:T001

    output_dir: Path = args.path.resolve()
    output_dir.mkdir(exist_ok=True, parents=True)

    # Captured frame includes white padding, so image size needs to be scaled to account
    pixel_size = args.size // marker_type.min_marker_image_size
    required_size = args.size + (pixel_size * 2)

    if args.size + args.border_size * 2 > min(page_size.value):
        print(  # noqa:T001
            f"Warning: Marker size is too large to fit on {args.page_size}"
        )
    elif required_size + args.border_size * 2 > min(page_size.value):
        print(  # noqa:T001
            f"Warning: Marker size is too large to fit on {args.page_size} with border"
        )

    if (
        args.border_size
        and args.center_line_length
        and args.border_size > args.center_line_length
    ):
        print("Warning: center lines may not be visible")  # noqa:T001

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
            image = Image.fromarray(camera.capture_frame())

            # Resize the image to the required size
            resized_image = image.resize([mm_to_pixels(required_size)] * 2, resample=0)

            # Add a border to the marker, which includes padding
            bordered_image = ImageOps.expand(
                resized_image, border=args.border_size, fill=BORDER_FILL
            )
            img_size = bordered_image.size[0]

            image_draw = ImageDraw.Draw(bordered_image)
            image_draw.text(
                (25, img_size - 25),
                args.description_format.format(
                    marker_type=marker_type.name, marker_id=marker_id
                ),
                anchor="lt",
            )

            # Add center lines
            if args.center_line_length:
                line_start = (img_size // 2) - (args.border_size // 2)

                # Top
                image_draw.line(
                    [line_start, 0, line_start, args.center_line_length],
                    width=args.border_size,
                    fill=BORDER_FILL,
                )

                # Left
                image_draw.line(
                    [0, line_start, args.center_line_length, line_start],
                    width=args.border_size,
                    fill=BORDER_FILL,
                )

                # Bottom
                image_draw.line(
                    [
                        line_start,
                        img_size - args.center_line_length,
                        line_start,
                        img_size,
                    ],
                    width=args.border_size,
                    fill=BORDER_FILL,
                )

                # Right
                image_draw.line(
                    [
                        img_size - args.center_line_length,
                        line_start,
                        img_size,
                        line_start,
                    ],
                    width=args.border_size,
                    fill=BORDER_FILL,
                )

            if args.force_a4:
                paper_img_1 = Image.new("RGB", PageSize.A4.pixels, (255, 255, 255))
                paper_img_2 = Image.new("RGB", PageSize.A4.pixels, (255, 255, 255))

                # Crop to just halves of the marker image
                image_half_top = bordered_image.crop((0, 0, img_size, img_size // 2))
                image_half_bottom = bordered_image.crop(
                    (0, img_size // 2, img_size, img_size)
                )

                # Rotate, so they fit better on the pages
                image_half_top = image_half_top.rotate(90, expand=True)
                image_half_bottom = image_half_bottom.rotate(90, expand=True)

                # Place images centered on page
                paper_img_1.paste(
                    image_half_top,
                    (
                        (PageSize.A4.pixels[0] - image_half_top.size[0]) // 2,
                        (PageSize.A4.pixels[1] - image_half_top.size[1]) // 2,
                    ),
                )
                paper_img_2.paste(
                    image_half_bottom,
                    (
                        (PageSize.A4.pixels[0] - image_half_bottom.size[0]) // 2,
                        (PageSize.A4.pixels[1] - image_half_bottom.size[1]) // 2,
                    ),
                )

                print("Saving marker", marker_id)  # noqa:T001
                paper_img_1.save(
                    output_dir / args.filename.format(id=marker_id),
                    quality=100,
                    dpi=(DPI, DPI),
                    save_all=True,
                    append_images=[
                        paper_img_2
                    ],  # Add the second image, resulting in a second page in the PDF
                )
            else:

                # Put marker onto page
                paper_img = Image.new("RGB", page_size.pixels, (255, 255, 255))
                paper_img.paste(
                    bordered_image,
                    (
                        (page_size.pixels[0] - img_size) // 2,
                        (page_size.pixels[1] - img_size) // 2,
                    ),
                )

                print("Saving marker", marker_id)  # noqa:T001
                paper_img.save(
                    output_dir / args.filename.format(id=marker_id),
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
        "--filename",
        type=str,
        help="Output filename. `id` is available for string format replacement (default: %(default)s)",
        default="{id}.pdf",
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
    parser.add_argument(
        "--force-a4",
        help="Output the PDF onto A4, splitting as necessary",
        action="store_true",
    )
    parser.add_argument(
        "--center-line-length",
        help="Length of center lines in pixels (default: %(default)s)",
        default=10,
        type=int,
    )
    parser.add_argument(
        "--border-size",
        help="Size of the border (and center lines) in pixels. Note that the border expands from center (default: %(default)s)",
        default=1,
        type=int,
    )
    parser.set_defaults(func=main)
