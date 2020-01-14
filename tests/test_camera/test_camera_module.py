import pytest

import zoloto.cameras


def test_exposes_camera():
    assert zoloto.cameras.Camera == zoloto.cameras.camera.Camera


@pytest.mark.parametrize("camera_name", ["ImageFileCamera", "VideoFileCamera"])
def test_exposes_file_camera(camera_name):
    assert getattr(zoloto.cameras, camera_name) == getattr(
        zoloto.cameras.file, camera_name
    )


def test_requires_abstract_arguments():
    class TestCamera(zoloto.cameras.Camera):
        pass

    with pytest.raises(TypeError) as e:
        TestCamera(0)
    assert (
        "Can't instantiate abstract class TestCamera with abstract methods"
        in e.value.args[0]
    )
