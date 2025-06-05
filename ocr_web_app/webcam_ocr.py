import cv2
import pytesseract


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to access the camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        text = pytesseract.image_to_string(frame)
        y0, dy = 30, 30
        for i, line in enumerate(text.split('\n')):
            y = y0 + i*dy
            cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Webcam OCR - Press q to quit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
