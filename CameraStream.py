import cv2
from threading import Thread
import time


class CameraStream:

    def __init__(self, src=0, width=1280, height=720):
        self.frame = None
        self.grabbed = None
        self.frame_operation = None
        self.frame_rate = 1 / 30
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, width)
        self.stream.set(4, height)
        self.get_frame()
        self.stopped = False
        self.disposed = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.disposed:
            time.sleep(self.frame_rate)
            if self.stopped:
                return
            self.get_frame()

    def get_frame(self):
        (self.grabbed, tmp) = self.stream.read()
        if getattr(self, 'frame_operation', None) is not None:
            self.frame = self.frame_operation(tmp)
        else:
            self.frame = tmp

    def stop(self):
        self.stopped = True

    def release(self):
        self.stopped = True
        self.disposed = True
        time.sleep(self.frame_rate * 2)
        self.stream.release()
