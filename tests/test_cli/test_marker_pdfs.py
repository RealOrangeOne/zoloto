from pathlib import Path

import pytest
from pdf2image import convert_from_path

from zoloto.cameras.file import ImageFileCamera
from zoloto.marker_type import MarkerType

from . import call_cli


def test_creates_correct_number_of_pdfs(tmp_path: Path) -> None:
    rtn = call_cli(["marker-pdfs", "APRILTAG_16H5", str(tmp_path), "100"])
    rtn.check_returncode()
    pdfs = list(tmp_path.glob("*.pdf"))
    assert len(pdfs) == MarkerType.APRILTAG_16H5.marker_count


@pytest.mark.parametrize("marker_type", MarkerType)
def test_detectable(marker_type: MarkerType, tmp_path: Path) -> None:
    rtn = call_cli(
        ["marker-pdfs", marker_type.name, str(tmp_path), "100", "--range", "0"]
    )
    rtn.check_returncode()
    convert_from_path(tmp_path / "0.pdf")[0].save(tmp_path / "0.png")
    image_file_camera = ImageFileCamera(tmp_path / "0.png", marker_type=marker_type)
    assert image_file_camera.get_visible_markers() == [0]
