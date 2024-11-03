import cv2
import tkinter as tk
from threading import Thread

from .color_recognition import ColorRecognition


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Autonomous Drone")

        self.start_button = tk.Button(self.root, text="Start Detection", command=self.start_detection)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Detection", command=self.stop_detection)
        self.stop_button.pack()

        self.running = False
        self.thread = None

        self.cr = ColorRecognition("src/color_bounds.json")

        print("App initialized")

    def start_detection(self):
        self.running = True
        self.thread = Thread(target=self.run_detection)
        self.thread.start()

    def stop_detection(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def run_detection(self):
        cap = cv2.VideoCapture(0)

        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Webcam", frame)

            detected_colors = self.cr.detect_colors(frame)
            cv2.imshow("Detected Colors", detected_colors)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        self.root.mainloop()