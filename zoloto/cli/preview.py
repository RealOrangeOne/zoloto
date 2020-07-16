import argparse

from zoloto.cameras.camera import Camera
from zoloto.marker_type import MarkerType
from zoloto.viewer import CameraViewer


class PreviewCamera(Camera):
    def get_marker_size(self, marker_id: int) -> int:
        return 100


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=0)
    args = parser.parse_args()
    with PreviewCamera(args.id, marker_type=MarkerType.DICT_6X6_250) as camera:
        CameraViewer(camera, annotate=True).start()


if __name__ == "__main__":
    main()
