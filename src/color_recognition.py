import cv2
import json
import numpy as np


class ColorRecognition:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_color_bounds()

    def load_color_bounds(self) -> None:
        with open(self.file_path, "r") as file:
            data = json.load(file)
            self.color_bounds = [(np.array(bound["lower"]), np.array(bound["upper"])) for bound in data]
            self.color_names = [color["name"] for color in data]

    def detect_color(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for lower, upper in self.color_bounds:
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame