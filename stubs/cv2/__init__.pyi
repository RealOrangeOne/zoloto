"""
Type stubs for cv2.
Note that stubs are only written for the parts that we use.
"""
from typing import List, Optional, Tuple, Union

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

def imread(path: str) -> ndarray: ...
def copyMakeBorder(
    src: ndarray,
    top: int,
    bottom: int,
    left: int,
    right: int,
    borderType: int,
    value: Optional[List[int]],
) -> ndarray: ...
