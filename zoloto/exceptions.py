from __future__ import annotations

from numpy.typing import NDArray


class ZolotoException(Exception):
    pass


class MissingCalibrationsError(ZolotoException):
    pass


class CameraReadError(ZolotoException):
    def __init__(self, frame: NDArray | None):
        self.frame = frame
        super().__init__()
