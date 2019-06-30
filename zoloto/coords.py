from typing import NamedTuple

from coordinates import spaced_coordinate

Coordinates = spaced_coordinate("Coordinates", "xy")

Orientation = NamedTuple(
    "Orientation", [("rot_x", float), ("rot_y", float), ("rot_z", float)]
)

ThreeDCoordinates = spaced_coordinate("ThreeDCoordinates", "xyz")

Spherical = NamedTuple("Spherical", [("rot_x", float), ("rot_y", float), ("dist", int)])
