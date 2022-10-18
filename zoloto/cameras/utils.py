import warnings
from typing import Tuple

from cv2 import CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH, VideoCapture

from zoloto.calibration import CalibrationParameters


def get_video_capture_resolution(video_capture: VideoCapture) -> Tuple[int, int]:
    return (
        int(video_capture.get(CAP_PROP_FRAME_WIDTH)),
        int(video_capture.get(CAP_PROP_FRAME_HEIGHT)),
    )


def set_video_capture_resolution(
    video_capture: VideoCapture, resolution: Tuple[int, int]
) -> None:
    video_capture.set(CAP_PROP_FRAME_WIDTH, resolution[0])
    video_capture.set(CAP_PROP_FRAME_HEIGHT, resolution[1])

    set_resolution = get_video_capture_resolution(video_capture)

    if set_resolution != resolution:
        raise ValueError(
            f"{resolution} is not a valid resolution for this camera. {set_resolution} is, however."
        )


def validate_calibrated_video_capture_resolution(
    video_capture: VideoCapture,
    calibration_params: CalibrationParameters,
    *,
    override: bool = False,
) -> None:
    device_resolution = get_video_capture_resolution(video_capture)
    if device_resolution != calibration_params.resolution:
        if override:
            warnings.warn("Overriding camera resolution with calibrated resolution")
            set_video_capture_resolution(video_capture, calibration_params.resolution)
        else:
            raise ValueError(
                f"The resolution of the camera {device_resolution!r} differs "
                f"from the calibrated resolution {calibration_params.resolution!r}"
            )
