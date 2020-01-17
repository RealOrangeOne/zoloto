import pytest

import zoloto.cameras
from zoloto.marker_dict import MarkerDict


def test_exposes_camera():
    assert zoloto.cameras.Camera == zoloto.cameras.camera.Camera


@pytest.mark.parametrize("camera_name", ["ImageFileCamera", "VideoFileCamera"])
def test_exposes_file_camera(camera_name):
    assert getattr(zoloto.cameras, camera_name) == getattr(
        zoloto.cameras.file, camera_name
    )


def test_camera_requires_abstract_arguments():
    class TestCamera(zoloto.cameras.Camera):
        pass

    with pytest.raises(TypeError) as e:
        TestCamera(0)
    exception_message = e.value.args[0]
    assert (
        "Can't instantiate abstract class TestCamera with abstract methods"
        in exception_message
    )
    assert "marker_dict" in exception_message
    assert "get_marker_size" in exception_message


def test_marker_camera_requires_abstract_arguments():
    class TestCamera(zoloto.cameras.marker.MarkerCamera):
        pass

    with pytest.raises(TypeError) as e:
        TestCamera(0, marker_size=200)
    exception_message = e.value.args[0]
    assert (
        "Can't instantiate abstract class TestCamera with abstract methods"
        in exception_message
    )
    assert "marker_dict" in exception_message
    assert "get_marker_size" not in exception_message


@pytest.mark.parametrize(
    "camera_class", [zoloto.cameras.Camera, zoloto.cameras.camera.SnapshotCamera]
)
def test_enumerate_all_cameras(camera_class, mocker):
    class TestCamera(camera_class):
        marker_dict = MarkerDict.DICT_4X4_100

        def get_marker_size(self, marker_id):
            return 100

    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = True
    discovered_cameras = list(TestCamera.discover())
    assert len(discovered_cameras) == 8
    for camera in discovered_cameras:
        assert isinstance(camera, TestCamera)


@pytest.mark.parametrize(
    "camera_class", [zoloto.cameras.Camera, zoloto.cameras.camera.SnapshotCamera]
)
def test_enumerate_no_cameras(camera_class, mocker):
    class TestCamera(camera_class):
        marker_dict = MarkerDict.DICT_4X4_100

        def get_marker_size(self, marker_id):
            return 100

    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = False
    discovered_cameras = list(TestCamera.discover())
    assert len(discovered_cameras) == 0


def test_get_camera_ids(mocker):
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = True
    discovered_ids = list(zoloto.cameras.camera.find_camera_ids())
    assert discovered_ids == [0, 1, 2, 3, 4, 5, 6, 7]


def test_get_no_camera_ids(mocker):
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = False
    discovered_ids = list(zoloto.cameras.camera.find_camera_ids())
    assert len(discovered_ids) == 0
