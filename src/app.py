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
from .models import Command, Line, Movement, Shape
from .camera_feed import CameraFeed
from .utils import combine_masks, gray2bgr


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
        self.line = Line()
        self.camera_feed = CameraFeed()
        self.shape_history = []

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

    @Slot(str)
    def command(self, command: str):
        if command == "land":
            self.drone.send_command(
                Command(type="action", action="land")
            )
        elif command == "takeoff":
            self.drone.send_command(
                Command(type="action", action="takeoff")
            )

    @Slot()
    def connect_drone(self):
        """Connects to the drone.

        Sends the `connect` command to the drone and emits the
        `isConnectedChanged` signal to update the UI. Handles exceptions
        if the connect command fails.
        """
        try:
            self.drone.connect()
            self.isConnectedChanged.emit()
        except Exception as e:
            print(f"Failed to connect to drone: {e}")

    @Slot()
    def disconnect_drone(self):
        """Disconnects from the drone.

        If the drone is processing, it stops the feed first. Then it can
        safely send the `disconnect` command to the drone. This ensures
        correct cleanup of resources and prevents any potential issues
        with the camera feed or processing thread. The method also emits
        the `isConnectedChanged` signal to update the UI. Handles
        exceptions if the disconnect command fails.
        """
        try:
            if self._is_processing:
                self.stop_feed()
            self.drone.disconnect()
            self.isConnectedChanged.emit()
        except Exception as e:
            print(f"Failed to disconnect from drone: {e}")

    @Slot()
    def start_feed(self):
        """Starts the camera feed and processing thread.

        Sends the `streamon` command to the drone and creates a new
        thread to process the feed. Emits the `isProcessingChanged`
        signal to update the UI. Handles exceptions if any of the
        mentioned steps fail.
        """
        try:
            self._is_processing = True
            self.drone.streamon()
            self._processing_thread = Thread(target=self.run_feed)
            self._processing_thread.start()
        except Exception as e:
            self._is_processing = False
            print(f"Failed to start feed: {e}")

        self.isProcessingChanged.emit()

    @Slot()
    def stop_feed(self):
        """Stops the camera feed and processing thread.

        Joins the processing thread and sends the `streamoff` command to
        the drone. Emits the `isProcessingChanged` signal to update the
        UI. Handles exceptions if any of the mentioned steps fail.
        """
        try:
            self._is_processing = False
            if self._processing_thread:
                self._processing_thread.join()
            self.drone.streamoff()
        except Exception as e:
            self._is_processing = True
            print(f"Failed to stop feed: {e}")

        self.isProcessingChanged.emit()

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
                    if not self.drone.is_flying:
                        self.drone.send_command(Command(
                            type="action",
                            action="takeoff"
                        ))

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

                    # Line following logic
                    self.line.update(mask_black)
                    line_data = self.line.data
                    angle = int(self.line.angle)
                    offset_x = line_data["center"][0] - frame.shape[1] // 2
                    offset_x_cm = int(self.drone.px_to_cm(-offset_x, frame.shape[1]))

                    if len(detected_shapes) == 0:
                        # Movement logic
                        if self.drone.height < 100:
                            self.drone.send_command(Command(
                                type="movement",
                                movement=Movement(x_axis=0, y_axis=0, z_axis=10, yaw=0)
                            ))
                        elif self.drone.height > 150:
                            self.drone.send_command(Command(
                                type="movement",
                                movement=Movement(x_axis=0, y_axis=0, z_axis=(-10), yaw=0)
                            ))
                        else:
                            if line_data["detected"]:
                                movement = Movement(x_axis=offset_x_cm, y_axis=10, z_axis=0, yaw=angle)
                                command = Command(type="movement", movement=movement)
                                self.drone.send_command(command)
                    else:
                        for detected_shape in detected_shapes:
                            shape_pos = detected_shape["position"]
                            for detected_color in detected_colors:
                                color_pos = detected_color["position"]
                                print(shape_pos, color_pos)
                                if shape_pos == color_pos:
                                    shape = Shape(
                                        name=detected_shape["name"],
                                        color=detected_color["name"]
                                    )
                                    print(f"Detected shape: {shape}")
                                    self.shape_history.append(shape)
                                    print(f"Shape history: {self.shape_history}")
                                    break

            if self._restart_windows == True:
                cv2.destroyAllWindows()
                self._restart_windows = False

            # Update and display the camera feed
            if self.camera_feed.mode == 1:
                self.camera_feed.frame = frame
                cv2.imshow("Drone Camera Feed", self.camera_feed.frame)
            elif self.camera_feed.mode == 2 and self._is_detecting:
                # Create a copy of the frame for debugging purposes
                debug_frame = frame.copy()

                # Add masks to highlight all detected colors
                mask = combine_masks(frame.shape[:2], mask_black, mask_colors)
                mask = gray2bgr(mask)
                debug_frame = cv2.addWeighted(mask, 0.75, debug_frame, 0.25, 0)

                # Add crosshair to the center of the frame
                cv2.line(debug_frame, (frame.shape[1] // 2, 0), (frame.shape[1] // 2, frame.shape[0]), (0, 255, 0), 1)
                cv2.line(debug_frame, (0, frame.shape[0] // 2), (frame.shape[1], frame.shape[0] // 2), (0, 255, 0), 1)

                # Add information about the line
                debug_frame = self.line.draw(debug_frame)

                # Visualize offset from the center of the line
                if line_data["detected"]:
                    cv2.line(
                        debug_frame,
                        (line_data["center"][0], line_data["center"][1] + 10),
                        (line_data["center"][0] - int(offset_x), line_data["center"][1] + 10),
                        (0, 0, 255),
                        2
                    )

                # Add px and cm above and below the line of the offset
                cv2.putText(debug_frame, f"{offset_x} px", (line_data["center"][0] - 50, line_data["center"][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.putText(debug_frame, f"{offset_x_cm:.2f} cm", (line_data["center"][0] - 50, line_data["center"][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                self.camera_feed.frame = debug_frame
                cv2.imshow("Debug Mode", self.camera_feed.frame)

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
