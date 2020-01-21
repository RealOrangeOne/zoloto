import signal
import tkinter
from types import FrameType
from typing import Tuple

import cv2
from numpy import ndarray
from PIL import Image
from PIL.ImageTk import PhotoImage

from zoloto.cameras.base import BaseCamera


class CameraViewer:
    def __init__(
        self,
        camera: BaseCamera,
        *,
        title: str = "Camera Viewer",
        annotate: bool = False
    ) -> None:
        self.camera = camera
        self.annotate = annotate
        self.window = tkinter.Tk()
        self.window.wm_title(title)
        self.window.resizable(False, False)
        self.window.geometry("{}x{}".format(*self.get_window_size(self.camera)))
        self.frame = tkinter.Frame(self.window)
        self.frame.pack()
        self.label = tkinter.Label(self.frame)
        self.label.pack()

        signal.signal(signal.SIGINT, self.signal_handler)

    def show_frame(self) -> None:
        frame = self.camera.capture_frame()
        if self.annotate:
            self.camera._annotate_frame(frame)
        frame = self.on_frame(frame)
        tkinter_image = PhotoImage(
            image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))
        )
        self.label.imagetk = tkinter_image  # type: ignore
        self.label.configure(image=tkinter_image)
        self.label.after(10, self.show_frame)

    def signal_handler(self, sig: signal.Signals, frame: FrameType) -> None:
        self.stop()

    def on_frame(self, frame: ndarray) -> ndarray:
        return frame

    def start(self) -> None:
        self.show_frame()
        self.window.mainloop()

    def stop(self) -> None:
        self.window.quit()  # type: ignore

    @staticmethod
    def get_window_size(camera: BaseCamera) -> Tuple[int, int]:
        shape = camera.capture_frame().shape
        return shape[1], shape[0]
