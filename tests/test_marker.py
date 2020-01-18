import json
from unittest import TestCase
from unittest.mock import patch

import ujson
from pytest import approx, raises

from zoloto.cameras.marker import MarkerCamera as BaseMarkerCamera
from zoloto.exceptions import MissingCalibrationsError
from zoloto.marker import Marker
from zoloto.marker_dict import MarkerDict


class MarkerTestCase(TestCase):
    MARKER_SIZE = 200
    MARKER_ID = 25

    def setUp(self):
        class MarkerCamera(BaseMarkerCamera):
            marker_dict = MarkerDict.DICT_6X6_50

        self.marker_camera = MarkerCamera(self.MARKER_ID, marker_size=self.MARKER_SIZE)
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
        self.assertEqual(tl, (border_size, border_size))
        self.assertEqual(tr, (self.MARKER_SIZE + border_size - 1, border_size))
        self.assertEqual(
            br,
            (self.MARKER_SIZE + border_size - 1, self.MARKER_SIZE + border_size - 1),
        )
        self.assertEqual(bl, (border_size, self.MARKER_SIZE + border_size - 1))

    def test_pixel_centre(self):
        tl, _, br, _ = self.marker.pixel_corners
        self.assertEqual(self.marker.pixel_centre, (139, 139))

    def test_distance(self):
        self.assertEqual(self.marker.distance, 992)

    def test_orientation(self):
        rot_x, rot_y, rot_z = self.marker.orientation
        self.assertEqual(int(rot_x), -3)
        self.assertEqual(int(rot_y), 0)
        self.assertEqual(int(rot_z), 0)

    def test_cartesian_coordinates(self):
        x, y, z = self.marker.cartesian
        self.assertEqual(int(x), 49)
        self.assertEqual(int(y), 24)
        self.assertEqual(int(z), 991)

    def test_spherical_coordinates(self):
        rot_x, rot_y, dist = self.marker.spherical
        self.assertEqual(dist, self.marker.distance)
        self.assertEqual(rot_x, approx(0.025, abs=1e-3))
        self.assertEqual(rot_y, approx(0.05, abs=1e-3))

    def test_as_dict(self):
        marker_dict = self.marker.as_dict()
        self.assertIsInstance(marker_dict, dict)
        self.assertEqual(
            {"id", "size", "pixel_corners", "rvec", "tvec"}, set(marker_dict.keys())
        )
        self.assertEqual(marker_dict["size"], self.MARKER_SIZE)
        self.assertEqual(marker_dict["id"], self.MARKER_ID)

    def test_dict_as_json(self):
        marker_dict = self.marker.as_dict()
        created_marker_dict = json.loads(json.dumps(marker_dict))
        self.assertEqual(marker_dict, created_marker_dict)

    def test_many_as_ujson(self):
        created_markers_dict = ujson.loads(
            ujson.dumps([m.as_dict() for m in self.markers])
        )
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
        class MarkerCamera(BaseMarkerCamera):
            marker_dict = MarkerDict.DICT_6X6_50

        self.marker_camera = MarkerCamera(self.MARKER_ID, marker_size=self.MARKER_SIZE)
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
        class MarkerCamera(BaseMarkerCamera):
            marker_dict = MarkerDict.DICT_6X6_50

        self.marker_camera = MarkerCamera(self.MARKER_ID, marker_size=self.MARKER_SIZE)
        self.markers = list(self.marker_camera.process_frame())
        self.marker = Marker.from_dict(self.markers[0].as_dict())


class MarkerSansCalibrationsTestCase(MarkerTestCase):
    class TestCamera(BaseMarkerCamera):
        marker_dict = MarkerDict.DICT_6X6_50

        def get_calibrations(self):
            return None

    def setUp(self):
        self.marker_camera = self.TestCamera(
            self.MARKER_ID, marker_size=self.MARKER_SIZE,
        )
        self.markers = list(self.marker_camera.process_frame())
        self.marker = self.markers[0]

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if name in [
            "test_orientation",
            "test_distance",
            "test_cartesian_coordinates",
            "test_spherical_coordinates",
        ]:

            def test_raises(*args, **kwargs):
                with raises(MissingCalibrationsError):
                    attr(*args, **kwargs)

            return test_raises
        return attr

    def test_as_dict(self):
        marker_dict = self.marker.as_dict()
        self.assertIsInstance(marker_dict, dict)
        self.assertEqual({"id", "size", "pixel_corners"}, set(marker_dict.keys()))
        self.assertEqual(marker_dict["size"], self.MARKER_SIZE)
        self.assertEqual(marker_dict["id"], self.MARKER_ID)

    def test_dict_as_ujson(self):
        marker_dict = self.marker.as_dict()
        created_marker_dict = ujson.loads(ujson.dumps(marker_dict))
        self.assertEqual(marker_dict["id"], created_marker_dict["id"])
        self.assertEqual(marker_dict["size"], created_marker_dict["size"])
        for expected_corner, corner in zip(
            marker_dict["pixel_corners"], created_marker_dict["pixel_corners"]
        ):
            self.assertEqual(expected_corner, approx(corner))
        self.assertNotIn("rvec", created_marker_dict)
        self.assertNotIn("tvec", created_marker_dict)


class MarkerSansCalibrationsFromDictTestCase(MarkerSansCalibrationsTestCase):
    def setUp(self):
        self.marker_camera = self.TestCamera(
            self.MARKER_ID, marker_size=self.MARKER_SIZE,
        )
        self.markers = list(self.marker_camera.process_frame())
        self.marker = Marker.from_dict(self.markers[0].as_dict())

    def test_is_not_eager(self):
        self.assertFalse(self.marker._is_eager())
