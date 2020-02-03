from abc import ABC, abstractmethod
from typing import Generator

from numpy import ndarray

from zoloto.exceptions import CameraReadError


class IterableCameraMixin(ABC):
    @abstractmethod
    def capture_frame(self) -> ndarray:  # pragma: nocover
        raise NotImplementedError()

    def __iter__(self) -> Generator[ndarray, None, None]:
        while True:
            frame = self.capture_frame()
            if not frame.size:
                break
            yield frame


class VideoCaptureMixin(ABC):
    def capture_frame(self) -> ndarray:
        ret, frame = self.video_capture.read()  # type: ignore
        if not ret or frame is None:
            raise CameraReadError(frame)
        return frame
