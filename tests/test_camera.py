from cv2 import aruco
from hypothesis import given

from tests import BaseTestCase
from tests.strategies import reasonable_image_size
from yuri import camera


class MarkerCameraTestCase(BaseTestCase):
    @given(reasonable_image_size())
    def test_captures_frame_at_correct_resolution(self, resolution):
        frame = camera.MarkerCamera(aruco.DICT_6X6_50, 25, resolution).capture_frame()
        self.assertEqual(frame.shape, (resolution, resolution))
