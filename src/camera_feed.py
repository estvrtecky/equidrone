import cv2
import numpy as np

from .utils import Config


MODE_OFF = 0
MODE_ON = 1
MODE_DEBUG = 2

class CameraFeed:
    def __init__(self):
        self.config = Config("config.ini")

        self.resolution = tuple(map(
            int,
            self.config.get("CameraFeed", "resolution").split("x")
        ))
        self._frame = np.zeros(
            (self.resolution[1], self.resolution[0], 3),
            dtype=np.uint8
        )
        self._mode = self.config.getint("CameraFeed", "mode")

    @property
    def frame(self) -> np.ndarray:
        return self._frame

    @frame.setter
    def frame(self, frame: np.ndarray) -> None:
        if frame is not None:
            if not isinstance(frame, np.ndarray):
                raise ValueError("Frame must be a NumPy array")
            self._frame = self.scale_frame(frame)

    @property
    def mode(self) -> int:
        return self._mode

    @mode.setter
    def mode(self, mode: int) -> None:
        if mode not in [MODE_OFF, MODE_ON, MODE_DEBUG]:
            raise ValueError("Invalid mode")
        self._mode = mode

    def pad_frame(self, frame: np.ndarray, target: tuple[int, int]) -> np.ndarray:
        """Pads the frame to the target resolution."""
        target_width, target_height = target
        frame_height, frame_width = frame.shape[:2]
        pad_width = (target_width - frame_width) // 2
        pad_height = (target_height - frame_height) // 2
        padded_frame = cv2.copyMakeBorder(frame, pad_height, pad_height, pad_width, pad_width, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        return padded_frame

    def scale_frame(self, frame: np.ndarray) -> np.ndarray:
        """Scales the frame to the configured resolution."""
        frame = frame.copy()

        camera_width, camera_height = self.resolution
        frame_height, frame_width = frame.shape[:2]
        camera_ratio = camera_width / camera_height
        frame_ratio = frame_width / frame_height

        if camera_ratio > frame_ratio:
            scale = camera_height / frame_height
            interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
            new_width = int(frame_width * scale)
            frame = cv2.resize(src=frame, dsize=(new_width, camera_height), interpolation=interpolation)
        elif camera_ratio < frame_ratio:
            scale = camera_width / frame_width
            interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
            new_height = int(frame_height * scale)
            frame = cv2.resize(src=frame, dsize=(camera_width, new_height), interpolation=interpolation)
        else:
            frame = cv2.resize(src=frame, dsize=(camera_width, camera_height), interpolation=cv2.INTER_AREA)

        frame = self.pad_frame(frame, self.resolution)

        return frame
