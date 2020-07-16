import pytest
from hypothesis import given, strategies

from tests.strategies import reasonable_image_size
from zoloto.cameras.file import ImageFileCamera
from zoloto.cameras.marker import MarkerCamera
from zoloto.exceptions import MissingCalibrationsError
from zoloto.marker import EagerMarker
from zoloto.marker_type import MarkerType


@given(reasonable_image_size())
def test_captures_frame_at_correct_resolution(resolution) -> None:
    marker_camera = MarkerCamera(
        25, marker_size=resolution, marker_type=MarkerType.DICT_6X6_50
    )
    frame = marker_camera.capture_frame()
    assert frame.shape == marker_camera.get_resolution()


@given(strategies.integers(0, 49))
def test_detects_markers(marker_id) -> None:
    markers = list(
        MarkerCamera(
            marker_id, marker_size=200, marker_type=MarkerType.DICT_6X6_50
        ).process_frame()
    )
    assert len(markers) == 1
    assert markers[0].id == marker_id


@given(strategies.integers(0, 49))
def test_detects_marker_ids(marker_id) -> None:
    markers = MarkerCamera(
        marker_id, marker_size=200, marker_type=MarkerType.DICT_6X6_50
    ).get_visible_markers()
    assert markers == [marker_id]


@given(strategies.integers(0, 49))
def test_eager_capture(marker_id) -> None:
    markers = list(
        MarkerCamera(
            marker_id, marker_size=200, marker_type=MarkerType.DICT_6X6_50
        ).process_frame_eager()
    )
    assert len(markers) == 1
    assert markers[0].id == marker_id
    assert isinstance(markers[0], EagerMarker)


def test_camera_as_context_manager() -> None:
    with MarkerCamera(
        25, marker_size=200, marker_type=MarkerType.DICT_6X6_50
    ) as marker_camera:
        markers = list(marker_camera.get_visible_markers())
        assert markers == [25]


def test_marker_with_falsy_id() -> None:
    with MarkerCamera(
        0, marker_size=200, marker_type=MarkerType.DICT_6X6_50
    ) as marker_camera:
        markers = list(marker_camera.get_visible_markers())
        assert markers == [0]


@given(strategies.integers(0, 49))
def test_saved_image(temp_image_file, marker_id) -> None:
    class TestImageCamera(ImageFileCamera):
        def get_marker_size(self, marker_id):
            return 200

    marker_camera = MarkerCamera(
        marker_id, marker_size=200, marker_type=MarkerType.DICT_6X6_50
    )
    marker_camera.save_frame(temp_image_file)
    image_file_camera = TestImageCamera(
        temp_image_file, marker_type=MarkerType.DICT_6X6_50
    )
    assert image_file_camera.get_visible_markers() == [marker_id]


@given(strategies.integers(0, 49))
def test_saved_image_with_annotation(temp_image_file, marker_id) -> None:
    marker_camera = MarkerCamera(
        marker_id, marker_size=200, marker_type=MarkerType.DICT_6X6_50
    )
    output_file = temp_image_file
    marker_camera.save_frame(output_file, annotate=True)


def test_process_eager_frame_without_calibrations() -> None:
    class TestCamera(MarkerCamera):
        def get_calibrations(self):
            return None

    marker_camera = TestCamera(25, marker_size=200, marker_type=MarkerType.DICT_6X6_50)
    with pytest.raises(MissingCalibrationsError):
        list(marker_camera.process_frame_eager())
