import sys
from pathlib import Path

from cv2 import (
    CAP_PROP_FPS,
    CAP_PROP_FRAME_HEIGHT,
    CAP_PROP_FRAME_WIDTH,
    VideoWriter,
    VideoWriter_fourcc,
)
from numpy import ndarray

from zoloto.cameras.file import VideoFileCamera
from zoloto.marker_type import MarkerType
from zoloto.viewer import CameraViewer


class TestCamera(VideoFileCamera):
    marker_type = MarkerType.DICT_6X6_50

    def get_marker_size(self, marker_id: int) -> int:
        return 100


class TestViewer(CameraViewer):
    counter = 0

    def on_frame(self, frame: ndarray) -> ndarray:
        self.counter += 1
        camera._annotate_frame(frame)
        writer.write(frame)
        print(self.counter, end="\r")  # noqa: T001
        return frame


with TestCamera(Path(sys.argv[1])) as camera:

    fps = camera.video_capture.get(CAP_PROP_FPS)
    frame_width = int(camera.video_capture.get(CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.video_capture.get(CAP_PROP_FRAME_HEIGHT))
    writer = VideoWriter(
        sys.argv[2],
        VideoWriter_fourcc("m", "p", "4", "v"),
        int(fps),
        (frame_width, frame_height),
    )
    TestViewer(camera).start()
    writer.release()
