from abc import ABC, abstractmethod
from typing import Generator

from cv2 import imshow, waitKey
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


class ViewableCameraMixin(ABC):
    @abstractmethod
    def __iter__(self) -> Generator[ndarray, None, None]:  # pragma: nocover
        raise NotImplementedError()

    @abstractmethod
    def _annotate_frame(self, frame: ndarray) -> None:  # pragma: nocover
        raise NotImplementedError()

    def show(self, annotate: bool = False) -> None:
        for frame in self:
            if annotate:
                self._annotate_frame(frame)
            imshow("camera", frame)
            waitKey(1)
