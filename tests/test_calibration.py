from pathlib import Path

import pytest

from zoloto.calibration import parse_calibration_file


def test_loading_missing_file() -> None:
    filename = Path("doesnt-exist.xml")
    assert not filename.exists()
    with pytest.raises(FileNotFoundError):
        parse_calibration_file(filename)


def test_loading_example(fixtures_dir: Path) -> None:
    calibrations = parse_calibration_file(
        fixtures_dir / "example-calibreation-params.xml"
    )

    assert calibrations.camera_matrix.tolist() == [
        [1.2519588293098975e03, 0, 6.6684948780852471e02],
        [0, 1.2519588293098975e03, 3.6298123112613683e02],
        [0, 0, 1],
    ]

    assert calibrations.distance_coefficients.tolist() == [
        [
            1.3569117181595716e-01,
            -8.2513063822554633e-01,
            0,
            0,
            1.6412101575010554e00,
        ]
    ]

    assert calibrations.resolution == (1280, 720)
