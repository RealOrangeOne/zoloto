from pathlib import Path
from typing import Callable

import pytest

from zoloto.calibration import (
    SUPPORTED_EXTENSIONS,
    get_fake_calibration_parameters,
    parse_calibration_file,
    save_calibrations,
)


@pytest.mark.parametrize("extension", SUPPORTED_EXTENSIONS)
def test_saving_calibrations(
    extension: str, make_temp_file: Callable[[str], Path]
) -> None:
    original_params = get_fake_calibration_parameters()
    calibrations_file = Path(make_temp_file("." + extension))
    save_calibrations(original_params, calibrations_file)
    read_params = parse_calibration_file(calibrations_file)
    assert read_params[0].tolist() == original_params[0].tolist()
    assert read_params[1].tolist() == original_params[1].tolist()


def test_cant_load_invalid_extension(make_temp_file: Callable[[str], Path]) -> None:
    with pytest.raises(ValueError) as e:
        parse_calibration_file(Path(make_temp_file(".unknown")))
    assert "Unknown calibration file format" in e.value.args[0]


def test_cant_save_invalid_extension() -> None:
    with pytest.raises(ValueError) as e:
        save_calibrations(get_fake_calibration_parameters(), Path("test.unknown"))
    assert "Unknown calibration file format" in e.value.args[0]


@pytest.mark.parametrize("extension", ["xml", "json"])
def test_loading_missing_file(extension: str) -> None:
    filename = Path("doesnt-exist." + extension)
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
