from typing import NamedTuple

Coordinates = NamedTuple("Coordinates", [("x", float), ("y", float)])

Orientation = NamedTuple(
    "Orientation", [("rot_x", float), ("rot_y", float), ("rot_z", float)]
)

ThreeDCoordinates = NamedTuple(
    "ThreeDCoordinates", [("x", float), ("y", float), ("z", float)]
)

Spherical = NamedTuple("Spherical", [("rot_x", float), ("rot_y", float), ("dist", int)])
