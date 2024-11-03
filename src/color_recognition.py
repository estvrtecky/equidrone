import cv2
import json
import numpy as np


class ColorRecognition:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.color_bounds = []
        self.color_names = []
        self.load_color_bounds()

    def load_color_bounds(self) -> None:
        """
        Loads color bounds from a JSON file.
        """
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.color_bounds = [(np.array(bound["lower"]), np.array(bound["upper"])) for bound in data]
                self.color_names = [color["name"] for color in data]
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            print(f"An error occurred while decoding JSON file: {self.file_path}")

    def apply_mask(self, hsv: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
        """
        Applies a mask to the HSV image based on the provided lower and upper HSV bounds.

        This function handles the case where the hue range wraps around the 0-179 range in HSV color space.
        """
        lower_hue = lower[0]
        upper_hue = upper[0]

        if lower_hue > upper_hue:
            mask1 = cv2.inRange(hsv, lower, np.array([179, upper[1], upper[2]]))
            mask2 = cv2.inRange(hsv, np.array([0, lower[1], lower[2]]), upper)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv, lower, upper)

        return mask

    def detect_colors(self, frame):
        frame = frame.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for (lower, upper), color_name in zip(self.color_bounds, self.color_names):
            mask = self.apply_mask(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return frame