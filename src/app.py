import cv2
import numpy as np
import sys
from threading import Thread
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from .color_recognition import ColorRecognition
from .shape_recognition import ShapeRecognition
from .drone import Drone


class App(QObject):
    def __init__(self):
        super().__init__()
        self.app = QGuiApplication()
        self.engine = QQmlApplicationEngine()

        self.running = False
        self.detection_thread = None

        self.cr = ColorRecognition()
        self.sr = ShapeRecognition()
        self.drone = Drone()

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

    @Slot()
    def start_detection(self):
        if not self.running:
            self.running = True
            self.detection_thread = Thread(target=self.run_detection)
            self.detection_thread.start()

    @Slot()
    def stop_detection(self):
        if self.running:
            self.running = False
            if self.detection_thread:
                self.detection_thread.join()

    def run_detection(self):
        self.drone.connect()

        while self.running:
            frame = self.drone.get_frame()

            # Display the original frame
            cv2.imshow("Drone camera feed", frame)

            detected_colors = self.cr.detect_colors(frame)

            # Display detected colors on the frame
            frame_colors = frame.copy()
            for color in detected_colors:
                x, y, w, h = color["position"]
                cv2.putText(frame_colors, color["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.rectangle(frame_colors, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Detected Colors", frame_colors)

            # Combined mask for all detected colors except black
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            for color in detected_colors:
                if color["name"] != "black":
                    mask = cv2.bitwise_or(mask, color["mask"])
            cv2.imshow("Combined Mask", mask)

            # Detect shapes in the combined mask and display it
            detected_shapes = self.sr.detect_shapes(mask)
            frame_shapes = frame.copy()
            for shape in detected_shapes:
                x, y, w, h = shape["position"]
                cv2.putText(frame_shapes, shape["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.rectangle(frame_shapes, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Detected Shapes", frame_shapes)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def run(self):
        sys.exit(self.app.exec())
