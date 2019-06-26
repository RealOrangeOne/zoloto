import pkg_resources

from zoloto.exceptions import MissingGUIComponents

__version__ = pkg_resources.require("zoloto")[0].version


def has_gui_components():
    try:
        pkg_resources.require("opencv-contrib-python")
        return True
    except pkg_resources.DistributionNotFound:
        return False


def assert_has_gui_components():
    if not has_gui_components():
        raise MissingGUIComponents()
