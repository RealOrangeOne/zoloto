import zoloto


def test_exposes_version():
    assert hasattr(zoloto, "__version__")
