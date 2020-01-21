"""
Type stubs for pyquaternion.
Note that stubs are only written for the parts that we use.
"""
from typing import Tuple, overload

from numpy import ndarray

class Quaternion:
    @overload
    def __init__(self, *, matrix: ndarray) -> None: ...
    @overload
    def __init__(self, *, axis: Tuple[float, float, float], scalar: float) -> None: ...
    @property
    def rotation_matrix(self) -> ndarray: ...
    @property
    def vector(self) -> ndarray: ...
    @property
    def yaw_pitch_roll(self) -> Tuple[float, float, float]: ...
