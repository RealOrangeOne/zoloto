import os
from tempfile import mkstemp

from tests import BaseTestCase
from yuri.calibration import (
    get_fake_calibration_parameters,
    parse_calibration_file,
    save_calibrations,
)


class CalibrationsFileTestCase(BaseTestCase):
    def test_saving_calibrations_json(self):
        original_params = get_fake_calibration_parameters(200)
        handle, calibrations_file = mkstemp(".json")
        os.close(handle)
        save_calibrations(original_params, calibrations_file)
        read_params = parse_calibration_file(calibrations_file)
        self.assertEqual(read_params[0].tolist(), original_params[0].tolist())
        self.assertEqual(read_params[1].tolist(), original_params[1].tolist())
        os.remove(calibrations_file)

    def test_saving_calibrations_xml(self):
        original_params = get_fake_calibration_parameters(200)
        handle, calibrations_file = mkstemp(".xml")
        os.close(handle)
        save_calibrations(original_params, calibrations_file)
        read_params = parse_calibration_file(calibrations_file)
        self.assertEqual(read_params[0].tolist(), original_params[0].tolist())
        self.assertEqual(read_params[1].tolist(), original_params[1].tolist())
        os.remove(calibrations_file)
