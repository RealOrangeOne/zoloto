import yuri


def test_exposes_version():
    assert hasattr(yuri, "__version__")
