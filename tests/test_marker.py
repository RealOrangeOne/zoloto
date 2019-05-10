from cv2 import aruco

from tests import BaseTestCase
from yuri.camera import MarkerCamera


class MarkerTestCase(BaseTestCase):
    MARKER_SIZE = 200
    MARKER_ID = 25

    def setUp(self):
        self.marker_camera = MarkerCamera(
            self.MARKER_ID, marker_dict=aruco.DICT_6X6_50, marker_size=self.MARKER_SIZE
        )
        self.markers = self.marker_camera.process_frame()
        self.assertEqual(len(self.markers), 1)
        self.marker = self.markers[0]

    def test_marker_size(self):
        self.assertEqual(self.marker.size, self.MARKER_SIZE)

    def test_marker_id(self):
        self.assertEqual(self.marker.id, self.MARKER_ID)
