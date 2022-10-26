from __future__ import annotations

from pathlib import Path

from zoloto.marker_type import MarkerType

from . import call_cli


def test_creates_correct_number_of_pdfs(tmp_path: Path) -> None:
    rtn = call_cli(["marker-pdfs", "APRILTAG_16H5", str(tmp_path), "100"])
    rtn.check_returncode()
    pdfs = list(tmp_path.glob("*.pdf"))
    assert len(pdfs) == MarkerType.APRILTAG_16H5.marker_count
