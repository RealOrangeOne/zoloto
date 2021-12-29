import argparse
from pathlib import Path

import cv2

from zoloto.cameras.file import VideoFileCamera
from zoloto.marker_type import MARKER_TYPE_NAMES, MarkerType


def main(args: argparse.Namespace) -> None:
    from tqdm import tqdm

    with VideoFileCamera(
        Path(args.in_file), marker_type=MarkerType[args.type], marker_size=100
    ) as camera:
        fps = camera.video_capture.get(cv2.CAP_PROP_FPS)
        frames = camera.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        width, height = camera.get_resolution()

        output_writer = cv2.VideoWriter(
            str(args.out_file),
            cv2.VideoWriter_fourcc(*"MP4V"),
            fps,
            [int(width), int(height)],
        )

        for frame in tqdm(camera, total=frames):
            camera._annotate_frame(frame)
            output_writer.write(frame)

        output_writer.release()


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("annotate-video", description="Annotate a video")
    parser.add_argument("in_file", type=str, help="")
    parser.add_argument("out_file", type=str, help="Output file (.mp4)")
    parser.add_argument(
        "--type",
        type=str,
        default=MarkerType.ARUCO_6X6.name,
        choices=sorted(MARKER_TYPE_NAMES),
        help="Marker dictionary",
    )
    parser.set_defaults(func=main)
