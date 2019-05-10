import os
from tempfile import mkstemp

from hypothesis import given, strategies

from tests import BaseTestCase
from yuri.calibration import (
    CalibrationParameters,
    parse_calibration_file,
    save_calibrations,
)


class CalibrationsFileTestCase(BaseTestCase):
    @given(
        strategies.lists(strategies.integers(), min_size=1),
        strategies.lists(strategies.integers(), min_size=1),
    )
    def test_loading_and_saving_json(self, in1, in2):
        original_params = CalibrationParameters(in1, in2)
        handle, calibrations_file = mkstemp(".json")
        os.close(handle)
        save_calibrations(original_params, calibrations_file)
        read_params = parse_calibration_file(calibrations_file)
        self.assertEqual(read_params[0].tolist(), original_params[0])
        self.assertEqual(read_params[1].tolist(), original_params[1])
        os.remove(calibrations_file)
