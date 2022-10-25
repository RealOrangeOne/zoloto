from pathlib import Path

import cv2
import pytest

from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_type import MarkerType

from . import call_cli


@pytest.mark.parametrize("marker_type", MarkerType)
def test_detectable(marker_type: MarkerType, tmp_path: Path) -> None:
    rtn = call_cli(
        [
            "marker-pdfs",
            marker_type.name,
            str(tmp_path),
            "100",
            "--range",
            "0",
            "--filename",
            "{id}.png",  # HACK: Pretend the output is a PNG for the sake of tests
        ]
    )
    rtn.check_returncode()

    class CustomImageCamera(ImageFileCamera):
        def get_detector_params(self) -> cv2.aruco_DetectorParameters:
            """
            Slightly tweak `minMarkerDistanceRate` to prevent the border superseding
            the marker edge during contour refinement.

            In reality, the border is removed during adaptive thresholding,
            however this isn't possible given just the PDF page.
            """
            detector_params = super().get_detector_params()
            detector_params.minMarkerDistanceRate = 0.035
            return detector_params

    image_file_camera = CustomImageCamera(tmp_path / "0.png", marker_type=marker_type)
    assert image_file_camera.get_visible_markers() == [0]


@pytest.mark.parametrize("marker_type", MarkerType)
def test_detectable_without_border(marker_type: MarkerType, tmp_path: Path) -> None:
    """
    Confirm that, if the border is removed, the marker is detected.

    In reality, the border is removed during adaptive thresholding,
    however this isn't possible given just the PDF page.
    """
    rtn = call_cli(
        [
            "marker-pdfs",
            marker_type.name,
            str(tmp_path),
            "100",
            "--range",
            "0",
            "--border-size",
            "0",
            "--filename",
            "{id}.png",  # HACK: Pretend the output is a PNG for the sake of tests
        ]
    )
    rtn.check_returncode()
    image_file_camera = ImageFileCamera(tmp_path / "0.png", marker_type=marker_type)
    assert image_file_camera.get_visible_markers() == [0]
