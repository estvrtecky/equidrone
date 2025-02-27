import cv2
import tkinter as tk
from threading import Thread

from .color_recognition import ColorRecognition
from .shape_recognition import ShapeRecognition


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

        self.cr = ColorRecognition()
        self.sr = ShapeRecognition()

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

            detected_colors = self.cr.detect_colors(frame)

            # Original frame
            cv2.imshow("Webcam", frame)

            # Display detected colors on the frame
            frame_colors = frame.copy()
            for color in detected_colors:
                x, y, w, h = color["position"]
                cv2.putText(frame_colors, color["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.rectangle(frame_colors, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Detected Colors", frame_colors)
            # Display masks for detected colors
            # for color in detected_colors:
            #     cv2.imshow(color["name"], color["mask"])

            # Combined mask for all detected colors except black
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            for color in detected_colors:
                if color["name"] != "black":
                    mask = cv2.bitwise_or(mask, color["mask"])
            cv2.imshow("Combined Mask", mask)

            # Detect shapes in the combined mask and display it
            shapes = self.sr.detect_shapes(mask)
            highlighted_frame = frame.copy()
            for shape in shapes:
                contour = shape["contour"]
                cv2.drawContours(highlighted_frame, [contour], -1, (0, 255, 0), 2)
                cv2.putText(highlighted_frame, shape["shape"], tuple(contour[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow("Detected Shapes", highlighted_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        self.root.mainloop()