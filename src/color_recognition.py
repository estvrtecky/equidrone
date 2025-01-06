import cv2
import json
import numpy as np


class ColorRecognition:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.color_bounds = []
        self.color_names = []
        self.load_color_bounds()

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

    def detect_colors(self, frame: np.ndarray) -> list[dict]:
        frame = frame.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        detected_colors = []
        for (lower, upper), color_name in zip(self.color_bounds, self.color_names):
            mask = self.apply_mask(hsv, lower, upper)
            mask = self.remove_noise(mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Get the largest contour and its area
                contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(contour)

                if area > 500:
                    # Create a mask with only the largest contour filled
                    mask = np.zeros_like(mask)
                    cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

                    x, y, w, h = cv2.boundingRect(contour)
                    detected_colors.append({
                        "name": color_name,
                        "position": (x, y, w, h),
                        "mask": mask
                    })

        return detected_colors

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

    def remove_noise(self, mask: np.ndarray) -> np.ndarray:
        """
        Removes noise from the mask using morphological operations.
        """
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return mask