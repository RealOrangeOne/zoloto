import pkg_resources

from zoloto.coords import Coordinates, Orientation, Spherical, ThreeDCoordinates  # noqa
from zoloto.exceptions import MissingGUIComponents
from zoloto.marker import Marker  # noqa
from zoloto.marker_dict import MarkerDict  # noqa

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
