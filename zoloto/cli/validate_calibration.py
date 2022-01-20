import argparse
import tempfile
from pathlib import Path
from typing import Optional

from zoloto.calibration import parse_calibration_file
from zoloto.cameras.file import ImageFileCamera
from zoloto.cameras.marker import MarkerCamera
from zoloto.marker_type import MarkerType


def is_valid_calibration(filename: Path) -> bool:
    if not filename.is_file():
        return False

    # First, Try and parse the file
    try:
        parse_calibration_file(filename)
    except (SystemError, ValueError):
        return False

    with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
        marker_camera = MarkerCamera(0, 200, marker_type=MarkerType.APRILTAG_36H11)
        marker_camera.save_frame(Path(temp_file.name))

        image_camera = ImageFileCamera(
            Path(temp_file.name),
            marker_size=200,
            marker_type=MarkerType.APRILTAG_36H11,
            calibration_file=filename,
        )

        # Sanity check the image camera
        if image_camera.get_visible_markers() != [0]:
            return False

        # Then, confirm the detection works
        if len(list(marker_camera.process_frame_eager())) != 1:
            return False

    return True


def main(args: argparse.Namespace) -> Optional[int]:
    if is_valid_calibration(args.file):
        print("Calibration is valid")  # noqa:T001
        return None
    else:
        print("Calibration is invalid")  # noqa:T001
        return 1


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "validate_calibration", description="Validate a calibration file"
    )
    parser.add_argument("file", type=Path, help="")
    parser.set_defaults(func=main)
