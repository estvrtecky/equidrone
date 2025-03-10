import cv2
import numpy as np
from djitellopy import Tello


class Drone:
    def __init__(self):
        self.drone = Tello()

    def connect(self):
        self.drone.connect()
        self.drone.streamon()

    def get_battery(self):
        return f"Battery: {self.drone.get_battery()}%"

    def get_frame(self) -> np.ndarray:
        """
        Returns a frame from the drone's camera.

        It converts the frame from RGB to BGR color space for compatibility with OpenCV.
        """
        frame = self.drone.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return frame