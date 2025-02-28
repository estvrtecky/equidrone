import cv2
import numpy as np

from .utils import Config


class ShapeRecognition:
    def __init__(self):
        self.config = Config("config.ini")
        self.stability_threshold = self.config.getint("ShapeRecognition", "stability_threshold")
        self.shape_proximity_threshold = self.config.getint("ShapeRecognition", "shape_proximity_threshold")
        self.tracked_shapes = []

    def detect_shapes(self, mask: np.ndarray) -> list[dict]:
        """
        Detects shapes in the provided mask.

        Returns a list of detected shapes. Each shape is represented as
        a dictionary containing the name of the shape and its position
        in the mask.
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            self.tracked_shapes.clear()

        for contour in contours:
            shape = {
                "name": self.identify_shape(contour),
                "position": cv2.boundingRect(contour),
                "counter": 0
            }
            if not self.is_tracked(shape):
                self.track_new_shape(shape)

            self.increase_counter(shape)

        shapes = [
            shape for shape in self.tracked_shapes if shape["counter"] == self.stability_threshold
        ]
        self.tracked_shapes = [
            shape for shape in self.tracked_shapes if shape["counter"] < self.stability_threshold
        ]

        return shapes

    def identify_shape(self, contour) -> str:
        """
        Identifies the shape of the contour based on the number of vertices.
        """
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 3:
            return "triangle"
        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / h
            return "square" if 0.95 <= aspect_ratio <= 1.05 else "rectangle"
        elif len(approx) > 4:
            return "circle"

    def is_close(self, shape1: dict, shape2: dict) -> bool:
        """
        Checks the proximity of two shapes based on their centers.
        """
        x1, y1, w1, h1 = shape1["position"]
        x2, y2, w2, h2 = shape2["position"]

        center1 = (x1 + w1 / 2, y1 + h1 / 2)
        center2 = (x2 + w2 / 2, y2 + h2 / 2)

        distance = np.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
        return distance <= self.shape_proximity_threshold

    def is_tracked(self, shape: dict) -> bool:
        """
        Checks if the shape is being tracked.
        """
        for tracked_shape in self.tracked_shapes:
            if shape["name"] == tracked_shape["name"] and self.is_close(shape, tracked_shape):
                return True
        return False

    def increase_counter(self, shape: dict) -> None:
        """
        Increases the counter of a tracked shape.
        """
        for tracked_shape in self.tracked_shapes:
            if shape["name"] == tracked_shape["name"] and self.is_close(shape, tracked_shape):
                tracked_shape["counter"] += 1

    def track_new_shape(self, shape: dict) -> None:
        """
        Adds a new shape to the list of tracked shapes.

        If the new shape is close to an already tracked shape, the
        existing tracked shape is updated instead of adding a duplicate.
        This prevents errors caused by temporary misidentifications.
        """
        for index, tracked_shape in enumerate(self.tracked_shapes):
            if self.is_close(shape, tracked_shape):
                self.tracked_shapes[index] = shape
                return

        self.tracked_shapes.append(shape)
