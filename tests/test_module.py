import zoloto


def test_exposes_version():
    assert hasattr(zoloto, "__version__")


def test_has_gui_components():
    assert not zoloto.has_gui_components()
