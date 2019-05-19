import numpy
from cv2 import aruco
from hypothesis import given, settings, strategies

from tests import BaseTestCase
from tests.strategies import reasonable_image_size
from yuri import camera


class MarkerCameraTestCase(BaseTestCase):
    @given(reasonable_image_size())
    def test_captures_frame_at_correct_resolution(self, resolution):
        marker_camera = camera.MarkerCamera(
            25, marker_dict=aruco.DICT_6X6_50, marker_size=resolution
        )
        frame = marker_camera.capture_frame()
        self.assertEqual(frame.shape, marker_camera.get_resolution())

    @given(strategies.integers(1, 49))  # TODO: 0 doesn't work for some reason
    @settings(deadline=None)
    def test_detects_markers(self, marker_id):
        markers = camera.MarkerCamera(
            marker_id, marker_dict=aruco.DICT_6X6_50, marker_size=200
        ).process_frame()
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0].id, marker_id)

    @given(strategies.integers(1, 49))  # TODO: 0 doesn't work for some reason
    @settings(deadline=None)
    def test_detects_marker_ids(self, marker_id):
        markers = camera.MarkerCamera(
            marker_id, marker_dict=aruco.DICT_6X6_50, marker_size=200
        ).get_visible_markers()
        self.assertEqual(markers, [marker_id])

    def test_sees_nothing_in_blank_image(self):
        marker_camera = camera.MarkerCamera(
            25, marker_dict=aruco.DICT_6X6_50, marker_size=200
        )
        empty_frame = numpy.zeros((200, 200, 3), numpy.uint8)
        markers = marker_camera.process_frame(frame=empty_frame)
        self.assertEqual(markers, [])

    @given(strategies.integers(1, 49))  # TODO: 0 doesn't work for some reason
    @settings(deadline=None)
    def test_eager_capture(self, marker_id):
        markers = camera.MarkerCamera(
            marker_id, marker_dict=aruco.DICT_6X6_50, marker_size=200
        ).process_frame_eager()
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0].id, marker_id)
        self.assertTrue(markers[0]._is_eager())
