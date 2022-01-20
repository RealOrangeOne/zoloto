from pathlib import Path
from typing import Callable

from zoloto.cli.validate_calibration import is_valid_calibration


def test_valid_calibration(fixtures_dir: Path) -> None:
    assert is_valid_calibration(fixtures_dir / "example-calibreation-params.xml")


def test_invalid_calibration(
    fixtures_dir: Path, make_temp_file: Callable[[str], Path]
) -> None:
    assert not is_valid_calibration(fixtures_dir / "missing.png")
    assert not is_valid_calibration(Path(make_temp_file(".png")))
    assert not is_valid_calibration(fixtures_dir / "missing.xml")
    assert not is_valid_calibration(Path(make_temp_file(".xml")))
