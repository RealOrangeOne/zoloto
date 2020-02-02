import sys
from pathlib import Path

from zoloto.cameras.file import VideoFileCamera
from zoloto.marker_dict import MarkerDict


def process_marker_dict(current_marker_dict: MarkerDict) -> None:
    class TestCamera(VideoFileCamera):
        marker_type = current_marker_dict

        def get_marker_size(self, marker_id: int) -> int:
            return 100

    found_markers = False
    with TestCamera(Path(sys.argv[1])) as camera:
        for i, frame in enumerate(camera):
            print(current_marker_dict, i, end="\r")  # noqa: T001
            if i % 3 == 0:
                if camera.get_visible_markers(frame=frame):
                    found_markers = True

    print(current_marker_dict, found_markers)  # noqa: T001


def main() -> None:
    for marker_dict in MarkerDict:
        process_marker_dict(marker_dict)


if __name__ == "__main__":
    main()
