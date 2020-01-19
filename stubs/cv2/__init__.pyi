"""
Type stubs for cv2.
Note that stubs are only written for the parts that we use.
"""
from typing import Tuple, Union

from numpy import ndarray

CAP_PROP_BUFFERSIZE: int

class aruco_DetectorParameters:
    pass

class VideoCapture:
    def __init__(self, camera_id: Union[int, str]) -> None: ...
    def isOpened(self) -> bool: ...
    def read(self) -> Tuple[bool, ndarray]: ...
    def release(self) -> None: ...
    def set(self, property: int, value: int) -> None: ...
