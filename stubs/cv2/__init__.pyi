"""
Type stubs for cv2.
Note that stubs are only written for the parts that we use.
"""
from typing import List, Optional, Tuple, Union

from numpy import array, ndarray

CAP_PROP_BUFFERSIZE: int
CAP_PROP_FPS: int
CAP_PROP_FRAME_HEIGHT: int
CAP_PROP_FRAME_WIDTH: int

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
    def write(self, nodename: str, data: array) -> None: ...

class VideoCapture:
    def __init__(self, camera_id: Union[int, str]) -> None: ...
    def isOpened(self) -> bool: ...
    def read(self) -> Tuple[bool, ndarray]: ...
    def release(self) -> None: ...
    def set(self, property: int, value: int) -> None: ...
    def get(self, property: int) -> float: ...

class VideoWriter_fourcc:
    def __init__(self, a: str, b: str, c: str, d: str) -> None: ...

class VideoWriter:
    def __init__(
        self, path: str, fourcc: VideoWriter_fourcc, fps: int, size: Tuple[int, int]
    ) -> None: ...
    def write(self, frame: ndarray) -> None: ...
    def release(self) -> None: ...

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
