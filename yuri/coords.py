from typing import NamedTuple

Coordinates = NamedTuple("Coordinates", [("x", int), ("y", int)])

Orientation = NamedTuple(
    "Orientation", [("rot_x", int), ("rot_y", int), ("rot_z", int)]
)

ThreeDCoordinates = NamedTuple(
    "ThreeDCoordinates", [("x", int), ("y", int), ("z", int)]
)
