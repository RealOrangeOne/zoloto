import json
from unittest import TestCase
from unittest.mock import patch

import ujson
from cv2 import aruco
from pytest import approx

from zoloto.cameras.marker import MarkerCamera
from zoloto.marker import Marker


class MarkerTestCase(TestCase):
    MARKER_SIZE = 200
    MARKER_ID = 25

    def setUp(self):
        self.marker_camera = MarkerCamera(
            self.MARKER_ID, marker_dict=aruco.DICT_6X6_50, marker_size=self.MARKER_SIZE
        )
        self.markers = list(self.marker_camera.process_frame())
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
        self.assertEqual(self.marker.pixel_centre.to_list(), [139, 139])

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

    def test_as_dict(self):
        marker_dict = self.marker.as_dict()
        self.assertIsInstance(marker_dict, dict)
        self.assertEqual(marker_dict["size"], self.MARKER_SIZE)
        self.assertEqual(marker_dict["id"], self.MARKER_ID)

    def test_dict_as_json(self):
        marker_dict = self.marker.as_dict()
        created_marker_dict = json.loads(json.dumps(marker_dict))
        self.assertEqual(marker_dict, created_marker_dict)

    def test_many_as_ujson(self):
        created_markers_dict = ujson.loads(ujson.dumps(self.markers))
        self.assertEqual(len(created_markers_dict), 1)
        self.assertEqual(
            {marker["id"] for marker in created_markers_dict}, {self.MARKER_ID}
        )

    def test_dict_as_ujson(self):
        marker_dict = self.marker.as_dict()
        created_marker_dict = ujson.loads(ujson.dumps(marker_dict))
        self.assertEqual(marker_dict["id"], created_marker_dict["id"])
        self.assertEqual(marker_dict["size"], created_marker_dict["size"])
        for expected_corner, corner in zip(
            marker_dict["pixel_corners"], created_marker_dict["pixel_corners"]
        ):
            self.assertEqual(expected_corner, approx(corner))
        self.assertEqual(marker_dict["rvec"], approx(created_marker_dict["rvec"]))
        self.assertEqual(marker_dict["tvec"], approx(created_marker_dict["tvec"]))


class EagerMarkerTestCase(MarkerTestCase):
    def setUp(self):
        self.marker_camera = MarkerCamera(
            self.MARKER_ID, marker_dict=aruco.DICT_6X6_50, marker_size=self.MARKER_SIZE
        )
        self.markers = list(self.marker_camera.process_frame_eager())
        self.marker = self.markers[0]

    def test_is_eager(self):
        self.assertTrue(self.marker._is_eager())

    @patch("cv2.aruco.estimatePoseSingleMarkers")
    def test_doesnt_calculate_pose(self, pose_mock):
        assert self.marker._tvec is not None
        assert self.marker._rvec is not None
        pose_mock.assert_not_called()


class MarkerFromDictTestCase(EagerMarkerTestCase):
    def setUp(self):
        self.marker_camera = MarkerCamera(
            self.MARKER_ID, marker_dict=aruco.DICT_6X6_50, marker_size=self.MARKER_SIZE
        )
        self.markers = list(self.marker_camera.process_frame())
        self.marker = Marker.from_dict(self.markers[0].as_dict())
