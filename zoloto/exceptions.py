from typing import Optional

from numpy import ndarray


class ZolotoException(Exception):
    pass


class MissingCalibrationsError(ZolotoException):
    pass


class CameraReadError(ZolotoException):
    def __init__(self, frame: Optional[ndarray]):
        self.frame = frame
        super().__init__()
