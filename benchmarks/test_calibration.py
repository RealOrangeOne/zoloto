from yuri.calibration import parse_calibration_file, save_calibrations


def test_save_calibrations_json(benchmark, fake_calibration_params, make_temp_file):
    benchmark(save_calibrations, fake_calibration_params, make_temp_file(".json"))


def test_save_calibrations_xml(benchmark, fake_calibration_params, make_temp_file):
    benchmark(save_calibrations, fake_calibration_params, make_temp_file(".xml"))


def test_parse_calibrations_xml(benchmark, fake_calibration_params, make_temp_file):
    temp_file = make_temp_file(".xml")
    save_calibrations(fake_calibration_params, temp_file)
    benchmark(parse_calibration_file.__wrapped__, temp_file)


def test_parse_calibrations_json(benchmark, fake_calibration_params, make_temp_file):
    temp_file = make_temp_file(".json")
    save_calibrations(fake_calibration_params, temp_file)
    benchmark(parse_calibration_file.__wrapped__, temp_file)
