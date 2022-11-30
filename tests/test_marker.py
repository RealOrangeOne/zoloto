from __future__ import annotations

import json
import math
from typing import Any
from unittest import TestCase
from unittest.mock import patch

from zoloto.cameras.marker import MarkerCamera
from zoloto.exceptions import MissingCalibrationsError
from zoloto.marker import BaseMarker, EagerMarker, UncalibratedMarker
from zoloto.marker_type import MAX_ALL_ALLOWED_ID, MarkerType


class MarkerTestCase(TestCase):
    MARKER_SIZE = 200
    MARKER_ID = MAX_ALL_ALLOWED_ID
    EXPECTED_DICT_KEYS = {"id", "size", "pixel_corners", "rvec", "tvec"}

    def setUp(self) -> None:
        self.marker_camera = MarkerCamera(
            self.MARKER_ID,
            marker_size=self.MARKER_SIZE,
            marker_type=MarkerType.ARUCO_6X6,
        )
        self.markers: list[BaseMarker] = list(self.marker_camera.process_frame())
        self.marker = self.markers[0]

    def assertIsType(self, a: Any, b: Any) -> None:
        self.assertEqual(type(a), b)

    def test_marker_size(self) -> None:
        self.assertEqual(self.marker.size, self.MARKER_SIZE)

    def test_marker_id(self) -> None:
        self.assertEqual(self.marker.id, self.MARKER_ID)

    def test_marker_type(self) -> None:
        self.assertEqual(self.marker.marker_type, MarkerType.ARUCO_6X6)

    def test_pixel_corners(self) -> None:
        self.assertEqual(len(self.marker.pixel_corners), 4)
        border_size = self.marker_camera.border_size
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
        self.assertAlmostEqual(
            self.marker.distance, 900, delta=100
        )  # HACK: Sometimes it changes

    def test_orientation(self) -> None:
        rot_x, rot_y, rot_z = self.marker.orientation
        self.assertIn(int(rot_x), [3, -3])  # HACK: Sometimes it changes
        self.assertEqual(int(rot_y), 0)
        self.assertEqual(int(rot_z), 0)

    def test_cartesian_coordinates(self) -> None:
        x, y, z = self.marker.cartesian
        self.assertAlmostEqual(int(x), 52, delta=10)  # HACK: Sometimes it changes
        self.assertAlmostEqual(int(y), 15, delta=20)  # HACK: Sometimes it changes
        self.assertAlmostEqual(int(z), 910, delta=100)  # HACK: Sometimes it changes

    def test_spherical_coordinates(self) -> None:
        dist, rot_x, rot_y = self.marker.spherical
        self.assertEqual(dist, self.marker.distance)
        self.assertAlmostEqual(rot_x, math.pi / 2, delta=0.1)
        self.assertAlmostEqual(rot_y, math.pi / 2, delta=0.1)

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
            self.assertIsType(self.marker.spherical.distance, int)

            self.assertIsType(self.marker.cartesian.x, float)
            self.assertIsType(self.marker.cartesian.y, float)
            self.assertIsType(self.marker.cartesian.z, float)

    def test_repr(self) -> None:
        self.assertIn(str(self.MARKER_ID), repr(self.marker))
        self.assertIn(str(self.MARKER_SIZE), repr(self.marker))
        self.assertIn("ARUCO_6X6", repr(self.marker))

        # Eager markers also show their distance
        if isinstance(self.marker, EagerMarker):
            self.assertIn(str(self.marker.distance), repr(self.marker))


class EagerMarkerTestCase(MarkerTestCase):
    def setUp(self) -> None:
        self.marker_camera = MarkerCamera(
            self.MARKER_ID,
            marker_size=self.MARKER_SIZE,
            marker_type=MarkerType.ARUCO_6X6,
        )
        self.markers = list(self.marker_camera.process_frame_eager())
        self.marker = self.markers[0]

    @patch("cv2.aruco.estimatePoseSingleMarkers")
    def test_doesnt_calculate_pose(self, pose_mock: Any) -> None:
        assert self.marker._tvec is not None
        assert self.marker._rvec is not None
        pose_mock.assert_not_called()

    def test_is_eager(self) -> None:
        self.assertIsInstance(self.marker, EagerMarker)


class UncalibratedMarkerTestCase(MarkerTestCase):
    EXPECTED_DICT_KEYS = {"id", "size", "pixel_corners"}

    def setUp(self) -> None:
        self.marker_camera = MarkerCamera(
            self.MARKER_ID,
            marker_size=self.MARKER_SIZE,
            marker_type=MarkerType.ARUCO_6X6,
        )
        self.marker_camera.calibration_params = None
        self.markers = list(self.marker_camera.process_frame())
        self.marker = self.markers[0]

    def test_is_uncalibrated(self) -> None:
        self.assertIsInstance(self.marker, UncalibratedMarker)
        with self.assertRaises(MissingCalibrationsError):
            self.marker._get_pose_vectors()

    def test_orientation(self) -> None:
        with self.assertRaises(MissingCalibrationsError):
            super().test_orientation()

    def test_distance(self) -> None:
        with self.assertRaises(MissingCalibrationsError):
            super().test_distance()

    def test_cartesian_coordinates(self) -> None:
        with self.assertRaises(MissingCalibrationsError):
            super().test_cartesian_coordinates()

    def test_spherical_coordinates(self) -> None:
        with self.assertRaises(MissingCalibrationsError):
            super().test_spherical_coordinates()
