from __future__ import annotations

from pathlib import Path

from zoloto.marker_type import MarkerType

from . import call_cli


def test_creates_correct_number_of_images(tmp_path: Path) -> None:
    rtn = call_cli(["save-markers", "APRILTAG_16H5", str(tmp_path)])
    rtn.check_returncode()
    pdfs = list(tmp_path.glob("*.png"))
    assert len(pdfs) == MarkerType.APRILTAG_16H5.marker_count
