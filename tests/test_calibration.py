from pathlib import Path

import pytest

from zoloto.calibration import (
    SUPPORTED_EXTENSIONS,
    get_fake_calibration_parameters,
    parse_calibration_file,
    save_calibrations,
)


@pytest.mark.parametrize("extension", SUPPORTED_EXTENSIONS)
def test_saving_calibrations(extension, make_temp_file):
    original_params = get_fake_calibration_parameters(200)
    calibrations_file = Path(make_temp_file("." + extension))
    save_calibrations(original_params, calibrations_file)
    read_params = parse_calibration_file(calibrations_file)
    assert read_params[0].tolist() == original_params[0].tolist()
    assert read_params[1].tolist() == original_params[1].tolist()


def test_cant_load_invalid_extension(make_temp_file):
    with pytest.raises(ValueError) as e:
        parse_calibration_file(Path(make_temp_file(".unknown")))
    assert "Unknown calibration file format" in e.value.args[0]


def test_cant_save_invalid_extension():
    with pytest.raises(ValueError) as e:
        save_calibrations(get_fake_calibration_parameters(200), Path("test.unknown"))
    assert "Unknown calibration file format" in e.value.args[0]


@pytest.mark.parametrize("extension", ["xml", "json"])
def test_loading_missing_file(extension):
    filename = Path("doesnt-exist." + extension)
    with pytest.raises(FileNotFoundError):
        parse_calibration_file(filename)
