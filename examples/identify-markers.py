import sys
from pathlib import Path

from zoloto.cameras.file import VideoFileCamera
from zoloto.marker_type import MarkerType


class TestCamera(VideoFileCamera):
    def get_marker_size(self, marker_id: int) -> int:
        return 100


def process_marker_type(current_marker_type: MarkerType) -> None:

    found_markers = False
    with TestCamera(Path(sys.argv[1]), marker_type=current_marker_type) as camera:
        for i, frame in enumerate(camera):
            print(current_marker_type, i, end="\r")  # noqa: T001
            if i % 3 == 0:
                if camera.get_visible_markers(frame=frame):
                    found_markers = True
                    break

    print(current_marker_type, found_markers)  # noqa: T001


def main() -> None:
    for marker_type in MarkerType:
        process_marker_type(marker_type)


if __name__ == "__main__":
    main()
