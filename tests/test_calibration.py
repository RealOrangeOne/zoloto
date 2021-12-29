from pathlib import Path
from typing import Callable

import pytest

from zoloto.calibration import (
    get_fake_calibration_parameters,
    parse_calibration_file,
    save_calibrations,
)


def test_saving_calibrations(make_temp_file: Callable[[str], Path]) -> None:
    original_params = get_fake_calibration_parameters()
    calibrations_file = Path(make_temp_file(".xml"))
    save_calibrations(original_params, calibrations_file)
    read_params = parse_calibration_file(calibrations_file)
    assert read_params.camera_matrix.tolist() == original_params[0].tolist()
    assert read_params.distance_coefficients.tolist() == original_params[1].tolist()


def test_loading_missing_file() -> None:
    filename = Path("doesnt-exist.xml")
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
