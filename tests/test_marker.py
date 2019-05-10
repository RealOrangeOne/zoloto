from cv2 import aruco

from tests import BaseTestCase
from yuri.camera import MarkerCamera
from yuri.coords import Coordinates


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

    def test_pixel_corners(self):
        self.assertEqual(len(self.marker.pixel_corners), 4)
        border_size = self.marker_camera.BORDER_SIZE
        tl, tr, br, bl = self.marker.pixel_corners
        self.assertEqual(tl, (border_size, border_size))
        self.assertEqual(tr, (self.MARKER_SIZE + border_size - 1, border_size))
        self.assertEqual(
            br, (self.MARKER_SIZE + border_size - 1, self.MARKER_SIZE + border_size - 1)
        )
        self.assertEqual(bl, (border_size, self.MARKER_SIZE + border_size - 1))

    def test_pixel_centre(self):
        tl, _, br, _ = self.marker.pixel_corners
        self.assertEqual(
            self.marker.pixel_centre,
            (tl.x + (self.MARKER_SIZE / 2) - 1, br.y - (self.MARKER_SIZE / 2)),
        )

    def test_distance(self):
        self.assertEqual(self.marker.distance, 992)
