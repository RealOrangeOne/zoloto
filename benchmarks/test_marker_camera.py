from __future__ import annotations

from pathlib import Path
from typing import Callable

from zoloto.cameras.marker import MarkerCamera


def test_process_frame_eager(benchmark: Callable, marker_camera: MarkerCamera) -> None:
    frame = marker_camera.capture_frame()
    benchmark(lambda: list(marker_camera.process_frame_eager(frame=frame)))


def test_process_frame(benchmark: Callable, marker_camera: MarkerCamera) -> None:
    frame = marker_camera.capture_frame()
    benchmark(lambda: list(marker_camera.process_frame(frame=frame)))


def test_capture_frame(benchmark: Callable, marker_camera: MarkerCamera) -> None:
    benchmark(marker_camera.capture_frame)


def test_get_visible_markers(benchmark: Callable, marker_camera: MarkerCamera) -> None:
    frame = marker_camera.capture_frame()
    benchmark(marker_camera.get_visible_markers, frame=frame)


def test_save_frame(
    benchmark: Callable, marker_camera: MarkerCamera, temp_image_file: Path
) -> None:
    benchmark(marker_camera.save_frame, temp_image_file)


def test_save_frame_with_annotation(
    benchmark: Callable, marker_camera: MarkerCamera, temp_image_file: Path
) -> None:
    benchmark(marker_camera.save_frame, temp_image_file, annotate=True)
