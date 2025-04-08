import cv2
import numpy as np


class Line:
    def __init__(self):
        self._detected = False
        self._center = (0, 0)
        self._angle = 0

    @property
    def detected(self) -> bool:
        return self._detected

    @property
    def center(self) -> tuple[int, int]:
        return self._center

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def data(self) -> dict:
        return {
            "detected": self._detected,
            "center": self._center,
            "angle": self._angle
        }

    def draw(self, frame: np.ndarray, offset_x: int, offset_x_cm: float) -> np.ndarray:
        """Draws the line information on the provided frame."""
        frame = frame.copy()

        if self._detected:
            # Draw the center of the line
            cv2.circle(frame, self._center, 5, (0, 0, 255), -1)

            # Display the angle of the line and visualize it
            cv2.putText(frame, f"Angle: {self._angle}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            x1 = int(self._center[0] - 100 * np.cos(self._angle * np.pi / 180))
            y1 = int(self._center[1] - 100 * np.sin(self._angle * np.pi / 180))
            x2 = int(self._center[0] + 100 * np.cos(self._angle * np.pi / 180))
            y2 = int(self._center[1] + 100 * np.sin(self._angle * np.pi / 180))
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Display the offset from the center
            cv2.line(
                frame,
                (self._center[0], self._center[1] + 10),
                (self._center[0] - offset_x, self._center[1] + 10),
                (0, 0, 255),
                2
            )

            cv2.putText(frame, f"{offset_x} px", (self._center[0] - 50, self._center[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, f"{offset_x_cm:.2f} cm", (self._center[0] - 50, self._center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return frame

    def update(self, mask: np.ndarray) -> None:
        """Updates the line information based on the provided mask."""

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            self._detected = False
            return
        else:
            self._detected = True
            contour = contours[0]

        M = cv2.moments(contour)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        self._center = (cx, cy)

        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        raw_angle = np.arctan2(vy, vx) * 180 / np.pi

        self._angle = (90 - raw_angle) % 180
        if self._angle > 90:
            self._angle -= 180
        self._angle = -self._angle
