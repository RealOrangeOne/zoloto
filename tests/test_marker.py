import json
from typing import Any, List, Optional
from unittest import TestCase
from unittest.mock import patch

import ujson
from pytest import approx

from zoloto.calibration import CalibrationParameters
from zoloto.cameras.marker import MarkerCamera as BaseMarkerCamera
from zoloto.exceptions import MissingCalibrationsError
from zoloto.marker import BaseMarker, UncalibratedMarker
from zoloto.marker_dict import MarkerDict


class MarkerTestCase(TestCase):
    MARKER_SIZE = 200
    MARKER_ID = 25
    EXPECTED_DICT_KEYS = {"id", "size", "pixel_corners", "rvec", "tvec"}

    def setUp(self) -> None:
        class MarkerCamera(BaseMarkerCamera):
            marker_dict = MarkerDict.DICT_6X6_50

        self.marker_camera = MarkerCamera(
            self.MARKER_ID, marker_size=self.MARKER_SIZE
        )  # type: BaseMarkerCamera
        self.markers = list(
            self.marker_camera.process_frame()
        )  # type: List[BaseMarker]
        self.marker = self.markers[0]

    def assertIsType(self, a: Any, b: Any) -> None:
        self.assertEqual(type(a), b)

    def test_marker_size(self) -> None:
        self.assertEqual(self.marker.size, self.MARKER_SIZE)

    def test_marker_id(self) -> None:
        self.assertEqual(self.marker.id, self.MARKER_ID)

    def test_marker_dict(self) -> None:
        self.assertEqual(self.marker.marker_dict, MarkerDict.DICT_6X6_50)

    def test_pixel_corners(self) -> None:
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

    def test_pixel_centre(self) -> None:
        tl, _, br, _ = self.marker.pixel_corners
        self.assertEqual(self.marker.pixel_centre, (139, 139))

    def test_distance(self) -> None:
        self.assertEqual(self.marker.distance, 992)

    def test_orientation(self) -> None:
        rot_x, rot_y, rot_z = self.marker.orientation
        self.assertEqual(int(rot_x), -3)
        self.assertEqual(int(rot_y), 0)
        self.assertEqual(int(rot_z), 0)

    def test_cartesian_coordinates(self) -> None:
        x, y, z = self.marker.cartesian
        self.assertEqual(int(x), 49)
        self.assertEqual(int(y), 24)
        self.assertEqual(int(z), 991)

    def test_spherical_coordinates(self) -> None:
        rot_x, rot_y, dist = self.marker.spherical
        self.assertEqual(dist, self.marker.distance)
        self.assertEqual(rot_x, approx(0.025, abs=1e-3))
        self.assertEqual(rot_y, approx(0.05, abs=1e-3))

    def test_as_dict(self) -> None:
        marker_dict = self.marker.as_dict()
        self.assertIsInstance(marker_dict, dict)
        self.assertEqual(self.EXPECTED_DICT_KEYS, set(marker_dict.keys()))
        self.assertEqual(marker_dict["size"], self.MARKER_SIZE)
        self.assertEqual(marker_dict["id"], self.MARKER_ID)

    def test_as_dict_json(self) -> None:
        marker_dict = self.marker.as_dict()
        created_marker_dict = json.loads(json.dumps(self.marker.as_dict()))
        self.assertEqual(marker_dict, created_marker_dict)
        self.assertEqual(self.EXPECTED_DICT_KEYS, set(marker_dict.keys()))

    def test_as_dict_ujson(self) -> None:
        created_marker_dict = ujson.loads(ujson.dumps(self.marker))
        self.assertEqual(self.EXPECTED_DICT_KEYS, set(created_marker_dict.keys()))

    def test_many_as_dict_ujson(self) -> None:
        created_marker_dict = ujson.loads(ujson.dumps(self.markers))
        self.assertEqual(self.EXPECTED_DICT_KEYS, set(created_marker_dict[0].keys()))

    def test_dict_value_types(self) -> None:
        marker_dict = self.marker.as_dict()
        self.assertIsType(marker_dict["id"], int)
        self.assertIsType(marker_dict["size"], int)

        pixel_corners = marker_dict["pixel_corners"]
        self.assertIsType(pixel_corners, list)
        self.assertIsType(pixel_corners[0], list)
        self.assertIsType(pixel_corners[0][0], float)

        if "rvec" in marker_dict:
            self.assertIsType(marker_dict["rvec"], list)
            self.assertIsType(marker_dict["rvec"][0], float)

            self.assertIsType(marker_dict["tvec"], list)
            self.assertIsType(marker_dict["tvec"][0], float)

    def test_marker_types(self) -> None:
        self.assertIsType(self.marker.id, int)
        self.assertIsType(self.marker.size, int)
        self.assertIsType(self.marker.pixel_corners[0].x, float)
        self.assertIsType(self.marker.pixel_corners[0].y, float)
        self.assertIsType(self.marker.pixel_centre.x, float)
        self.assertIsType(self.marker.pixel_centre.y, float)

        if "rvec" in self.EXPECTED_DICT_KEYS:
            self.assertIsType(self.marker.distance, int)

            self.assertIsType(self.marker.spherical.rot_x, float)
            self.assertIsType(self.marker.spherical.rot_y, float)
            self.assertIsType(self.marker.spherical.dist, int)

            self.assertIsType(self.marker.cartesian.x, float)
            self.assertIsType(self.marker.cartesian.y, float)
            self.assertIsType(self.marker.cartesian.z, float)


class EagerMarkerTestCase(MarkerTestCase):
    def setUp(self) -> None:
        class MarkerCamera(BaseMarkerCamera):
            marker_dict = MarkerDict.DICT_6X6_50

        self.marker_camera = MarkerCamera(self.MARKER_ID, marker_size=self.MARKER_SIZE)
        self.markers = list(self.marker_camera.process_frame_eager())
        self.marker = self.markers[0]

    @patch("cv2.aruco.estimatePoseSingleMarkers")
    def test_doesnt_calculate_pose(self, pose_mock: Any) -> None:
        assert self.marker._tvec is not None
        assert self.marker._rvec is not None
        pose_mock.assert_not_called()


class UncalibratedMarkerTestCase(MarkerTestCase):
    EXPECTED_DICT_KEYS = {"id", "size", "pixel_corners"}

    class TestCamera(BaseMarkerCamera):
        marker_dict = MarkerDict.DICT_6X6_50

        def get_calibrations(self) -> Optional[CalibrationParameters]:
            return None

    def setUp(self) -> None:
        self.marker_camera = self.TestCamera(
            self.MARKER_ID, marker_size=self.MARKER_SIZE,
        )
        self.markers = list(self.marker_camera.process_frame())
        self.marker = self.markers[0]

    def test_is_uncalibrated(self) -> None:
        self.assertIsInstance(self.marker, UncalibratedMarker)
        with self.assertRaises(MissingCalibrationsError):
            self.marker._get_pose_vectors()

    def __getattribute__(self, name: str) -> Any:
        attr = super().__getattribute__(name)
        if name in [
            "test_orientation",
            "test_distance",
            "test_cartesian_coordinates",
            "test_spherical_coordinates",
        ]:

            def test_raises(*args: Any, **kwargs: Any) -> None:
                with self.assertRaises(MissingCalibrationsError):
                    attr(*args, **kwargs)

            return test_raises
        return attr
