from typing import Type

import pytest
from hypothesis import given
from pytest_mock.plugin import MockerFixture

import zoloto.cameras
from tests.strategies import marker_types
from zoloto.exceptions import CameraOpenError
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


def test_cannot_create_unopened_camera(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = False
    with pytest.raises(CameraOpenError):
        zoloto.cameras.Camera(0, marker_type=MarkerType.APRILTAG_36H11)


def test_cannot_create_unopened_snapshotcamera(mocker: MockerFixture) -> None:
    VideoCapture = mocker.patch("zoloto.cameras.camera.VideoCapture")
    VideoCapture.return_value.isOpened.return_value = False
    camera = zoloto.cameras.camera.SnapshotCamera(
        0, marker_type=MarkerType.APRILTAG_36H11
    )
    with pytest.raises(CameraOpenError):
        camera.capture_frame()
