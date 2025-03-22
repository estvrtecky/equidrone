import cv2
import numpy as np
import sys
from threading import Thread
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from .color_recognition import ColorRecognition
from .shape_recognition import ShapeRecognition
from .drone import Drone
from .camera_feed import CameraFeed
from .utils import combine_masks


class App(QObject):
    def __init__(self):
        super().__init__()

        # Core properties
        self._is_processing = False
        self._is_detecting = False
        self._processing_thread = None
        self._restart_windows = False

        # App components
        self.cr = ColorRecognition()
        self.sr = ShapeRecognition()
        self.drone = Drone()
        self.camera_feed = CameraFeed()

        # App UI components
        self.app = QGuiApplication()
        self.engine = QQmlApplicationEngine()

        # Timer to update drone info
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_drone_info)
        self.update_timer.start(1000)

        # Set app icon based on system theme
        self.set_icon("src/ui/assets/logo.png", "src/ui/assets/logo-neg.png")

        # Expose the App object to QML before loading the QML file
        self.engine.rootContext().setContextProperty("app", self)

        # Load the QML file
        self.engine.load("src/ui/main.qml")

        # Check if the QML file is loaded successfully
        if not self.engine.rootObjects():
            print("Failed to load QML file!")
            sys.exit(-1)
        else:
            print("QML file loaded successfully")

    batteryLevelChanged = Signal()
    cameraFeedModeChanged = Signal()
    heightChanged = Signal()
    isConnectedChanged = Signal()
    isDetectingChanged = Signal()
    isProcessingChanged = Signal()
    temperatureChanged = Signal()

    @Property(int, notify=batteryLevelChanged)
    def battery_level(self):
        return self.drone.battery

    @Property(int, notify=cameraFeedModeChanged)
    def camera_feed_mode(self):
        return self.camera_feed.mode

    @camera_feed_mode.setter
    def camera_feed_mode(self, mode: int):
        if mode != self.camera_feed.mode:
            self.camera_feed.mode = mode
            self._restart_windows = True

    @Property(int, notify=heightChanged)
    def height(self):
        return self.drone.height

    @Property(bool, notify=isConnectedChanged)
    def is_connected(self):
        return self.drone.is_connected

    @Property(bool, notify=isDetectingChanged)
    def is_detecting(self):
        return self._is_detecting

    @Property(bool, notify=isProcessingChanged)
    def is_processing(self):
        return self._is_processing

    @Property(int, notify=temperatureChanged)
    def temperature(self):
        return self.drone.temperature

    @Slot()
    def connect_drone(self):
        try:
            self.drone.connect()
            self.isConnectedChanged.emit()
        except Exception as e:
            print(f"Failed to connect to drone: {e}")

    @Slot()
    def disconnect_drone(self):
        try:
            self.drone.disconnect()
            self.isConnectedChanged.emit()
        except Exception as e:
            print(f"Failed to disconnect from drone: {e}")

    @Slot()
    def start_feed(self):
        if not self._is_processing and self.drone.is_connected:
            try:
                self._is_processing = True
                self.drone.streamon()
                self._processing_thread = Thread(target=self.run_feed)
                self._processing_thread.start()
                self.isProcessingChanged.emit()
            except Exception as e:
                self._is_processing = False
                print(f"Failed to start feed: {e}")

    @Slot()
    def stop_feed(self):
        if self._is_processing:
            self._is_processing = False
            try:
                if self._processing_thread:
                    self._processing_thread.join()
                self.drone.streamoff()
                self.isProcessingChanged.emit()
            except Exception as e:
                self._is_processing = True
                print(f"Failed to stop feed: {e}")

    @Slot()
    def toggle_autopilot(self):
        self._is_detecting = not self._is_detecting
        self.isDetectingChanged.emit()

    def run(self):
        sys.exit(self.app.exec())

    def run_feed(self):
        while self._is_processing and self.drone.is_connected:
            # Get the current frame from the drone
            frame = self.drone.get_frame()

            # Flip the frame upside down
            if frame is not None:
                frame = cv2.flip(frame, 0)

                # Detection logic for autonomous flight
                if self._is_detecting:
                    # Detect colors in the frame
                    detected_colors = self.cr.detect_colors(frame)

                    # Split detected color masks into black and other colors
                    mask_black = combine_masks(
                        frame.shape[:2],
                        *[color["mask"] for color in detected_colors if color["name"] == "black"]
                    )

                    mask_colors = combine_masks(
                        frame.shape[:2],
                        *[color["mask"] for color in detected_colors if color["name"] != "black"]
                    )

                    # Display detected colors on the frame
                    frame_colors = frame.copy()
                    for color in detected_colors:
                        x, y, w, h = color["position"]
                        cv2.putText(frame_colors, color["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        cv2.rectangle(frame_colors, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Detect shapes in the combined mask and display it
                    detected_shapes = self.sr.detect_shapes(mask_colors)
                    frame_shapes = frame.copy()
                    for shape in detected_shapes:
                        x, y, w, h = shape["position"]
                        cv2.putText(frame_shapes, shape["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        cv2.rectangle(frame_shapes, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # TODO: Implement line following here

            if self._restart_windows == True:
                cv2.destroyAllWindows()
                self._restart_windows = False

            # Update and display the camera feed
            self.camera_feed.frame = frame
            if self.camera_feed.mode == 1:
                cv2.imshow("Drone Camera Feed", self.camera_feed.frame)
            elif self.camera_feed.mode == 2 and self._is_detecting:
                # TODO: Move debug windows to camera feed
                cv2.imshow("Black Mask", mask_black)
                cv2.imshow("Colors Mask", mask_colors)
                cv2.imshow("Detected Colors", frame_colors)
                cv2.imshow("Detected Shapes", frame_shapes)

            # TODO: Refactor this to just update the camera feed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def set_icon(self, light_icon_path: str, dark_icon_path: str) -> None:
        """Sets the application icon based on the system theme."""
        palette = self.app.palette()
        background_color = palette.window().color()
        is_dark = background_color.lightnessF() < 0.5

        if is_dark:
            self.app.setWindowIcon(QIcon(dark_icon_path))
        else:
            self.app.setWindowIcon(QIcon(light_icon_path))

    def update_drone_info(self):
        self.batteryLevelChanged.emit()
        self.temperatureChanged.emit()
        self.heightChanged.emit()
