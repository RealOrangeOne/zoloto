import pytest
from hypothesis import given

from tests.strategies import marker_ids, marker_types, reasonable_image_size
from zoloto.cameras.file import ImageFileCamera
from zoloto.cameras.marker import MarkerCamera
from zoloto.exceptions import MissingCalibrationsError
from zoloto.marker import EagerMarker
from zoloto.marker_type import MAX_ALL_ALLOWED_ID, MarkerType


@given(reasonable_image_size(), marker_types())
def test_captures_frame_at_correct_resolution(resolution, marker_type) -> None:
    marker_camera = MarkerCamera(25, marker_size=resolution, marker_type=marker_type)
    frame = marker_camera.capture_frame()
    assert frame.shape == marker_camera.get_resolution()


@pytest.mark.parametrize("marker_type", MarkerType)
@given(marker_ids())
def test_detects_markers(marker_type, marker_id) -> None:
    markers = list(
        MarkerCamera(
            marker_id, marker_size=100, marker_type=marker_type
        ).process_frame()
    )
    assert len(markers) == 1
    assert markers[0].id == marker_id


@pytest.mark.parametrize("marker_type", MarkerType)
@given(marker_ids())
def test_detects_marker_ids(marker_type, marker_id) -> None:
    markers = MarkerCamera(
        marker_id, marker_size=200, marker_type=marker_type
    ).get_visible_markers()
    assert markers == [marker_id]


@pytest.mark.parametrize("marker_type", MarkerType)
@given(marker_ids())
def test_eager_capture(marker_type, marker_id) -> None:
    markers = list(
        MarkerCamera(
            marker_id, marker_size=200, marker_type=marker_type
        ).process_frame_eager()
    )
    assert len(markers) == 1
    assert markers[0].id == marker_id
    assert isinstance(markers[0], EagerMarker)


@given(marker_types())
def test_camera_as_context_manager(marker_type) -> None:
    with MarkerCamera(
        MAX_ALL_ALLOWED_ID, marker_size=200, marker_type=marker_type
    ) as marker_camera:
        markers = list(marker_camera.get_visible_markers())
        assert markers == [MAX_ALL_ALLOWED_ID]


@given(marker_types())
def test_marker_with_falsy_id(marker_type) -> None:
    with MarkerCamera(0, marker_size=200, marker_type=marker_type) as marker_camera:
        markers = list(marker_camera.get_visible_markers())
        assert markers == [0]


@pytest.mark.parametrize("marker_type", MarkerType)
@given(marker_ids())
def test_saved_image(marker_type, temp_image_file, marker_id) -> None:
    marker_camera = MarkerCamera(marker_id, marker_size=200, marker_type=marker_type)
    marker_camera.save_frame(temp_image_file)
    image_file_camera = ImageFileCamera(
        temp_image_file, marker_type=marker_type, marker_size=200
    )
    assert image_file_camera.get_visible_markers() == [marker_id]


@pytest.mark.parametrize("marker_type", MarkerType)
@given(marker_ids())
def test_marker_size(marker_type, temp_image_file, marker_id) -> None:
    class TestCamera(ImageFileCamera):
        def get_marker_size(self, inner_marker_id: int) -> int:
            return inner_marker_id * 10

    marker_camera = MarkerCamera(marker_id, marker_size=200, marker_type=marker_type)
    marker_camera.save_frame(temp_image_file)
    image_file_camera = TestCamera(temp_image_file, marker_type=marker_type)
    marker = next(image_file_camera.process_frame())
    assert marker.size == marker_id * 10
    assert marker.id == marker_id


@given(marker_ids(), marker_types())
def test_saved_image_with_annotation(temp_image_file, marker_id, marker_type) -> None:
    marker_camera = MarkerCamera(marker_id, marker_size=200, marker_type=marker_type)
    output_file = temp_image_file
    marker_camera.save_frame(output_file, annotate=True)


@given(marker_types())
def test_process_eager_frame_without_calibrations(marker_type) -> None:
    class TestCamera(MarkerCamera):
        def get_calibrations(self):
            return None

    marker_camera = TestCamera(
        MAX_ALL_ALLOWED_ID, marker_size=200, marker_type=marker_type
    )
    with pytest.raises(MissingCalibrationsError):
        list(marker_camera.process_frame_eager())


@pytest.mark.parametrize("marker_type", MarkerType)
def test_requires_in_range_marker_id(marker_type) -> None:
    MarkerCamera(marker_type.max_id, marker_size=200, marker_type=marker_type)

    with pytest.raises(ValueError) as e:
        MarkerCamera(marker_type.max_id + 1, marker_size=200, marker_type=marker_type)

    assert "must be less than the maximum allowed" in e.value.args[0]


@pytest.mark.parametrize("marker_type", MarkerType)
def test_minimum_marker_size(marker_type) -> None:
    camera = MarkerCamera(
        marker_type.max_id,
        marker_size=marker_type.min_marker_size,
        marker_type=marker_type,
    )

    assert camera.get_visible_markers() == [marker_type.max_id]

    with pytest.raises(ValueError) as e:
        MarkerCamera(
            marker_type.max_id,
            marker_size=marker_type.min_marker_size - 1,
            marker_type=marker_type,
        )
    assert "marker must be at least" in e.value.args[0]
