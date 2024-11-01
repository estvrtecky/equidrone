import cv2
from color_recognition import ColorRecognition


def main():
    lower_red = [0, 100, 100]
    upper_red = [10, 255, 255]
    cr = ColorRecognition(lower_red, upper_red)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam", frame)

        processed_frame = cr.detect_color(frame)
        cv2.imshow("Frame with Contours", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()