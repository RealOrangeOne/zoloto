import pkg_resources

from zoloto.coords import Coordinates, Orientation, Spherical, ThreeDCoordinates
from zoloto.marker import Marker
from zoloto.marker_type import MarkerType

__version__ = pkg_resources.require("zoloto")[0].version  # type: str


__all__ = [
    "Coordinates",
    "Orientation",
    "Spherical",
    "ThreeDCoordinates",
    "MissingGUIComponents",
    "Marker",
    "MarkerType",
]
