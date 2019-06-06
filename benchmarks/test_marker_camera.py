def test_process_frame_eager(benchmark, marker_camera):
    frame = marker_camera.capture_frame()
    benchmark(lambda: list(marker_camera.process_frame_eager(frame)))


def test_process_frame(benchmark, marker_camera):
    frame = marker_camera.capture_frame()
    benchmark(lambda: list(marker_camera.process_frame(frame)))


def test_capture_frame(benchmark, marker_camera):
    benchmark(marker_camera.capture_frame)


def test_get_visible_markers(benchmark, marker_camera):
    frame = marker_camera.capture_frame()
    benchmark(marker_camera.get_visible_markers, frame=frame)


def test_save_frame(benchmark, marker_camera, make_temp_file):
    benchmark(marker_camera.save_frame, make_temp_file(".png"))


def test_save_frame_with_annotation(benchmark, marker_camera, make_temp_file):
    benchmark(marker_camera.save_frame, make_temp_file(".png"), annotate=True)
