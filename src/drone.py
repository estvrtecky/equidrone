import cv2
import numpy as np
from djitellopy import Tello

from .models import Command
from .utils import Config


class Drone:
    def __init__(self):
        self.config = Config("config.ini")

        self._is_connected = False
        self._is_flying = False

        self.drone = None
        self.fov_horizontal = self.config.getfloat("Drone", "fov_horizontal")
        self._frame_reader = None

    @property
    def battery(self) -> int:
        """
        Returns the battery level of the drone in percentage.
        """
        return self.drone.get_battery() if self._is_connected else 0

    @property
    def height(self) -> int:
        """
        Returns the actual height from the ground in centimeters usin
        the TOF sensor.
        """
        return self.drone.get_distance_tof() if self._is_connected else 0

    @property
    def is_connected(self) -> bool:
        """
        Returns whether the drone is connected or not.
        """
        return self._is_connected

    @property
    def is_flying(self) -> bool:
        """Returns whether the drone is flying or not."""
        return self._is_flying

    @property
    def temperature(self) -> float:
        """Returns the temperature of the drone in Celsius."""
        return self.drone.get_temperature() if self._is_connected else 0

    def connect(self):
        """Connects to the drone."""
        if not self._is_connected:
            self.drone = Tello()
            try:
                self.drone.connect()
                self._is_connected = True
                print("Drone successfully connected.")
            except Exception as e:
                self.drone = None
                self._is_connected = False
                raise RuntimeError(f"Failed to connect to drone: {e}")

    def disconnect(self):
        """Disconnects from the drone."""
        if self._is_connected:
            try:
                self.drone.end()
                self.drone = None
                self._is_connected = False
                print("Disconnected from drone.")
            except Exception as e:
                self._is_connected = True
                raise RuntimeError(f"Failed to disconnect from drone: {e}")

    def get_frame(self) -> np.ndarray | None:
        """Returns a frame from the drone's camera.

        It converts the frame from RGB to BGR color space for compatibility with OpenCV.
        """
        if self._is_connected and self._frame_reader:
            frame = self._frame_reader.frame
            if frame is not None:
                return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return None

    def px_to_cm(self, px: int, frame_width: int) -> float | None:
        """Converts pixels to centimeters based on the drone's camera FOV and height."""
        if self._is_connected:
            w_real = 2 * self.height * np.tan(self.fov_horizontal / 2)
            return w_real / frame_width * px
        return None

    def send_command(self, command: Command) -> str:
        """Sends a command to the drone."""
        if self._is_connected:
            try:
                command_type = command.type
                if command_type == "movement":
                    self.drone.send_rc_control(
                        command.movement.x_axis,
                        command.movement.y_axis,
                        command.movement.z_axis,
                        command.movement.yaw
                    )
                elif command_type == "action":
                    action = command.action
                    if action == "takeoff":
                        self.drone.takeoff()
                        self._is_flying = True
                    elif action == "land":
                        self.drone.land()
                        self._is_flying = False
            except Exception as e:
                raise RuntimeError(f"Failed to send command to drone: {e}")

    def streamon(self):
        """Starts the video stream from the drone."""
        if self._is_connected:
            try:
                self.drone.streamon()
                self._frame_reader = self.drone.get_frame_read()
                cv2.waitKey(1000)
                print("Video stream started.")
            except Exception as e:
                self._frame_reader = None
                raise RuntimeError(f"Failed to start video stream: {e}")

    def streamoff(self):
        """Stops the video stream from the drone."""
        if self._is_connected:
            try:
                self.drone.streamoff()
                while not self._frame_reader.stopped:
                    cv2.waitKey(100)
                print("Video stream stopped.")
            except Exception as e:
                raise RuntimeError(f"Failed to stop video stream: {e}")
