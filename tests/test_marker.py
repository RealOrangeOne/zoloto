from unittest import TestCase

from cv2 import aruco

from yuri.camera import MarkerCamera


class MarkerTestCase(TestCase):
    MARKER_SIZE = 200
    MARKER_ID = 25

    def setUp(self):
        self.marker_camera = MarkerCamera(
            self.MARKER_ID, marker_dict=aruco.DICT_6X6_50, marker_size=self.MARKER_SIZE
        )
        self.markers = list(self.marker_camera.process_frame())
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
        self.assertEqual(tl.to_list(), [border_size, border_size])
        self.assertEqual(
            tr.to_list(), [self.MARKER_SIZE + border_size - 1, border_size]
        )
        self.assertEqual(
            br.to_list(),
            [self.MARKER_SIZE + border_size - 1, self.MARKER_SIZE + border_size - 1],
        )
        self.assertEqual(
            bl.to_list(), [border_size, self.MARKER_SIZE + border_size - 1]
        )

    def test_pixel_centre(self):
        tl, _, br, _ = self.marker.pixel_corners
        self.assertEqual(
            self.marker.pixel_centre.to_list(),
            [tl.x + (self.MARKER_SIZE / 2) - 1, br.y - (self.MARKER_SIZE / 2)],
        )

    def test_distance(self):
        self.assertEqual(self.marker.distance, 992)

    def test_orientation(self):
        rot_x, rot_y, rot_z = self.marker.orientation
        self.assertEqual(int(rot_x), 3)
        self.assertEqual(int(rot_y), 0)
        self.assertEqual(int(rot_z), 0)

    def test_coordinates(self):
        x, y, z = self.marker.cartesian.values()
        self.assertEqual(int(x), 49)
        self.assertEqual(int(y), 24)
        self.assertEqual(int(z), 991)
