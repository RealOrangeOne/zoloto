from typing import NamedTuple

from coordinates import spaced_coordinate

Coordinates = spaced_coordinate("Coordinates", "xy")

Orientation = NamedTuple(
    "Orientation", [("rot_x", int), ("rot_y", int), ("rot_z", int)]
)

ThreeDCoordinates = spaced_coordinate("ThreeDCoordinates", "xyz")
