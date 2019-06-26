import pytest

import zoloto


def test_exposes_version():
    assert hasattr(zoloto, "__version__")


def test_has_gui_components():
    assert not zoloto.has_gui_components()


def test_assert_gui_components():
    with pytest.raises(zoloto.exceptions.MissingGUIComponents):
        zoloto.assert_has_gui_components()
