from typing import Optional

from numpy.typing import NDArray


class ZolotoException(Exception):
    pass


class MissingCalibrationsError(ZolotoException):
    pass


class CameraReadError(ZolotoException):
    def __init__(self, frame: Optional[NDArray]):
        self.frame = frame
        super().__init__()
