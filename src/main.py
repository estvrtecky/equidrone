import cv2
from color_recognition import ColorRecognition


def main():
    color_bounds = [
        ([0, 100, 100], [10, 255, 255]), # Red
        ([94, 80, 2], [126, 255, 255]), # Blue
        ([25, 52, 72], [102, 255, 255]), # Yellow
        ([35, 52, 72], [85, 255, 255]), # Green
        ([0, 0, 0], [180, 255, 30]) # Black
    ]

    cr = ColorRecognition(color_bounds)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam", frame)

        processed_frame = cr.detect_color(frame)
        cv2.imshow("Detected Colors", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()