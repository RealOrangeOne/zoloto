"""
Type stubs for cv2.
Note that stubs are only written for the parts that we use.
"""
from typing import List, Optional, Tuple, Union

from numpy import array, ndarray

CAP_PROP_BUFFERSIZE: int

FILE_STORAGE_READ: int
FILE_STORAGE_WRITE: int

class aruco_DetectorParameters:
    pass

class FileNode:
    def mat(self) -> array: ...

class FileStorage:
    def __init__(self, path: str, mode: int) -> None: ...
    def getNode(self, nodename: str) -> FileNode: ...
    def release(self) -> None: ...
    def write(self, nodename: str, data: array): ...

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

# Note that this is not the only signature of Rodrigues, but it is the only one we use.
def Rodrigues(vector: Tuple[float, float, float]) -> Tuple[ndarray, ndarray]: ...
