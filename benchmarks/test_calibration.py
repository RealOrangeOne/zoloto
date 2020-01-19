from pathlib import Path
from typing import Callable

from zoloto.calibration import (
    CalibrationParameters,
    parse_calibration_file,
    save_calibrations,
)


def test_save_calibrations_json(
    benchmark: Callable,
    fake_calibration_params: CalibrationParameters,
    make_temp_file: Callable[[str], Path],
) -> None:
    benchmark(save_calibrations, fake_calibration_params, Path(make_temp_file(".json")))


def test_save_calibrations_xml(
    benchmark: Callable,
    fake_calibration_params: CalibrationParameters,
    make_temp_file: Callable[[str], Path],
) -> None:
    benchmark(save_calibrations, fake_calibration_params, Path(make_temp_file(".xml")))


def test_parse_calibrations_xml(
    benchmark: Callable,
    fake_calibration_params: CalibrationParameters,
    make_temp_file: Callable[[str], Path],
) -> None:
    temp_file = Path(make_temp_file(".xml"))
    save_calibrations(fake_calibration_params, temp_file)
    benchmark(parse_calibration_file.__wrapped__, temp_file)


def test_parse_calibrations_json(
    benchmark: Callable,
    fake_calibration_params: CalibrationParameters,
    make_temp_file: Callable[[str], Path],
) -> None:
    temp_file = Path(make_temp_file(".json"))
    save_calibrations(fake_calibration_params, temp_file)
    benchmark(parse_calibration_file.__wrapped__, temp_file)
