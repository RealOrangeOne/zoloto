import yuri


def test_exposes_version():
    assert hasattr(yuri, "__version__")


def test_exposes_camera():
    assert yuri.Camera == yuri.camera.Camera
