def test_capture_frame(benchmark, image_file_camera):
    benchmark(image_file_camera.capture_frame)


def test_get_visible_markers(benchmark, image_file_camera):
    frame = image_file_camera.capture_frame()
    benchmark(image_file_camera.get_visible_markers, frame=frame)


def test_save_frame(benchmark, image_file_camera, make_temp_file):
    benchmark(image_file_camera.save_frame, make_temp_file(".png"))


def test_save_frame_with_annotation(benchmark, image_file_camera, make_temp_file):
    benchmark(image_file_camera.save_frame, make_temp_file(".png"), annotate=True)
