from typing import Type

import pytest
from cv2 import CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from hypothesis import given
from pytest_mock.plugin import MockerFixture

import zoloto.cameras
from tests.strategies import marker_types
from zoloto.marker_type import MarkerType


@pytest.mark.parametrize(
    "camera_class", [zoloto.cameras.Camera, zoloto.cameras.camera.SnapshotCamera]
)
@given(marker_types())
def test_enumerate_all_cameras(
    camera_class: Type[zoloto.cameras.Camera],
    mocker: MockerFixture,
    marker_type: MarkerType,
) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = True
    discovered_cameras = list(
        camera_class.discover(marker_type=marker_type, marker_size=100)
    )
    assert len(discovered_cameras) == 8
    for camera in discovered_cameras:
        assert isinstance(camera, camera_class)


@pytest.mark.parametrize(
    "camera_class", [zoloto.cameras.Camera, zoloto.cameras.camera.SnapshotCamera]
)
@given(marker_types())
def test_enumerate_no_cameras(
    camera_class: Type[zoloto.cameras.Camera],
    mocker: MockerFixture,
    marker_type: MarkerType,
) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = False
    discovered_cameras = list(
        camera_class.discover(marker_type=marker_type, marker_size=100)
    )
    assert len(discovered_cameras) == 0


def test_get_camera_ids(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = True
    discovered_ids = list(zoloto.cameras.camera.find_camera_ids())
    assert discovered_ids == [0, 1, 2, 3, 4, 5, 6, 7]


def test_get_no_camera_ids(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = False
    discovered_ids = list(zoloto.cameras.camera.find_camera_ids())
    assert len(discovered_ids) == 0


def test_validates_set_resolution(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.get.side_effect = [1920, 1080]
    camera = zoloto.cameras.Camera(0, marker_type=MarkerType.ARUCO_6X6)
    with pytest.raises(ValueError):
        camera.set_resolution((1280, 720))


def test_set_resolution(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.get.side_effect = [1920, 1080]
    camera = zoloto.cameras.Camera(0, marker_type=MarkerType.ARUCO_6X6)
    camera.set_resolution((1920, 1080))
    VideoCapture.return_value.set.assert_any_call(CAP_PROP_FRAME_WIDTH, 1920)
    VideoCapture.return_value.set.assert_any_call(CAP_PROP_FRAME_HEIGHT, 1080)


def test_set_resolution_during_construction(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.get.side_effect = [1920, 1080]
    zoloto.cameras.Camera(0, marker_type=MarkerType.ARUCO_6X6, resolution=(1920, 1080))
    VideoCapture.return_value.set.assert_any_call(CAP_PROP_FRAME_WIDTH, 1920)
    VideoCapture.return_value.set.assert_any_call(CAP_PROP_FRAME_HEIGHT, 1080)


def test_get_resolution(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.get.side_effect = [1920, 1080]
    camera = zoloto.cameras.Camera(0, marker_type=MarkerType.ARUCO_6X6)
    assert camera.get_resolution() == (1920, 1080)


def test_get_resolution_snapshot() -> None:
    camera = zoloto.cameras.camera.SnapshotCamera(
        0, marker_type=MarkerType.ARUCO_6X6, resolution=(1920, 1080)
    )
    assert camera.get_resolution() == (1920, 1080)


def test_set_resolution_snapshot() -> None:
    camera = zoloto.cameras.camera.SnapshotCamera(0, marker_type=MarkerType.ARUCO_6X6)
    camera.set_resolution((1920, 1080))
    assert camera.get_resolution() == (1920, 1080)
