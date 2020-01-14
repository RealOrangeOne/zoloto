import signal
import tkinter
from threading import Thread

import cv2
from PIL import Image, ImageTk

from zoloto.cameras.base import BaseCamera


class CameraViewer:
    def __init__(
        self,
        camera: BaseCamera,
        *,
        size=(600, 600),
        title="Camera Viewer",
        annotate=False
    ):
        self.camera = camera
        self.annotate = annotate
        self.window = tkinter.Tk()
        self.window.wm_title(title)
        self.window.geometry("{}x{}".format(*size))
        self.frame = tkinter.Frame(self.window)
        self.frame.pack()
        self.label = tkinter.Label(self.frame)
        self.label.pack()

        signal.signal(signal.SIGINT, self.signal_handler)

    def show_frame(self):
        frame = self.camera.capture_frame()
        if self.annotate:
            self.camera._annotate_frame(frame)
        new_frame = self.on_frame(frame)
        if new_frame is not None:
            frame = new_frame
        colour_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        window_size = (self.window.winfo_width(), self.window.winfo_height())
        tkinter_image = ImageTk.PhotoImage(
            image=Image.fromarray(colour_image).resize(window_size)
        )
        self.label.imagetk = tkinter_image
        self.label.configure(image=tkinter_image)
        self.label.after(10, self.show_frame)

    def signal_handler(self, sig, frame):
        self.stop()

    @staticmethod
    def on_frame(frame):
        return frame

    def start(self):
        self.show_frame()
        self.window.mainloop()

    def stop(self):
        self.window.quit()
