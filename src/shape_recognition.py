import cv2
import numpy as np


class ShapeRecognition:
    def __init__(self):
        pass

    def detect_shapes(self, mask: np.ndarray):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        shapes = []
        for contour in contours:
            shape = self.identify_shape(contour)
            if shape:
                shapes.append({
                    "shape": shape,
                    "contour": contour
                })

        return shapes

    def identify_shape(self, contour) -> str:
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
