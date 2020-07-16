import pytest

import zoloto.cameras


def test_exposes_camera() -> None:
    assert zoloto.cameras.Camera == zoloto.cameras.camera.Camera


@pytest.mark.parametrize("camera_name", ["ImageFileCamera", "VideoFileCamera"])
def test_exposes_file_camera(camera_name) -> None:
    assert getattr(zoloto.cameras, camera_name) == getattr(
        zoloto.cameras.file, camera_name
    )


def test_camera_requires_abstract_arguments() -> None:
    class TestCamera(zoloto.cameras.Camera):
        pass

    with pytest.raises(TypeError) as e:
        TestCamera(0)
    exception_message = e.value.args[0]
    assert (
        "Can't instantiate abstract class TestCamera with abstract methods"
        in exception_message
    )
    assert "marker_type" in exception_message
    assert "get_marker_size" in exception_message


def test_marker_camera_requires_abstract_arguments() -> None:
    class TestCamera(zoloto.cameras.marker.MarkerCamera):
        pass

    with pytest.raises(TypeError) as e:
        TestCamera(0, marker_size=200)
    exception_message = e.value.args[0]
    assert (
        "Can't instantiate abstract class TestCamera with abstract methods"
        in exception_message
    )
    assert "marker_type" in exception_message
    assert "get_marker_size" not in exception_message
