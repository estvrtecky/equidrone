import cv2
import numpy as np


class ColorRecognition:
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = np.array(lower_bound)
        self.upper_bound = np.array(upper_bound)

    def detect_color(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Filter small areas for more accuracy
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the mask
        cv2.imshow('Mask', mask)

        # Create a blank image to draw contours on
        contour_img = frame.copy()
        cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

        # Display the contours
        cv2.imshow('Contours', contour_img)

        return frame