import numpy
from cv2 import aruco
from hypothesis import given, settings, strategies

from tests.strategies import reasonable_image_size
from yuri import camera


@given(reasonable_image_size())
def test_captures_frame_at_correct_resolution(resolution):
    marker_camera = camera.MarkerCamera(
        25, marker_dict=aruco.DICT_6X6_50, marker_size=resolution
    )
    frame = marker_camera.capture_frame()
    assert frame.shape == marker_camera.get_resolution()


@given(strategies.integers(0, 49))
@settings(deadline=None)
def test_detects_markers(marker_id):
    markers = list(
        camera.MarkerCamera(
            marker_id, marker_dict=aruco.DICT_6X6_50, marker_size=200
        ).process_frame()
    )
    assert len(markers) == 1
    assert markers[0].id == marker_id


@given(strategies.integers(0, 49))
@settings(deadline=None)
def test_detects_marker_ids(marker_id):
    markers = camera.MarkerCamera(
        marker_id, marker_dict=aruco.DICT_6X6_50, marker_size=200
    ).get_visible_markers()
    assert markers == [marker_id]


def test_sees_nothing_in_blank_image():
    marker_camera = camera.MarkerCamera(
        25, marker_dict=aruco.DICT_6X6_50, marker_size=200
    )
    empty_frame = numpy.zeros((200, 200, 3), numpy.uint8)
    markers = list(marker_camera.process_frame(frame=empty_frame))
    assert markers == []


@given(strategies.integers(0, 49))
@settings(deadline=None)
def test_eager_capture(marker_id):
    markers = list(
        camera.MarkerCamera(
            marker_id, marker_dict=aruco.DICT_6X6_50, marker_size=200
        ).process_frame_eager()
    )
    assert len(markers) == 1
    assert markers[0].id == marker_id
    assert markers[0]._is_eager()


def test_camera_as_context_manager():
    with camera.MarkerCamera(
        25, marker_dict=aruco.DICT_6X6_50, marker_size=200
    ) as marker_camera:
        markers = list(marker_camera.get_visible_markers())
        assert markers == [25]


def test_marker_with_falsy_id():
    with camera.MarkerCamera(
        0, marker_dict=aruco.DICT_6X6_50, marker_size=200
    ) as marker_camera:
        markers = list(marker_camera.get_visible_markers())
        assert markers == [0]
