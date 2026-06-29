"""
Practical 05B: Count Faces in Video

Requirements:
    python -m pip install opencv-python numpy

Input:
    Place "people.mp4" in the same folder as this script, or edit VIDEO_PATH.
"""

from pathlib import Path

import cv2


# Original Colab path: /content/people.mp4
VIDEO_PATH = Path(__file__).with_name("people.mp4")


def main() -> None:
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {VIDEO_PATH}")

    detector = cv2.CascadeClassifier(
        str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
    )
    if detector.empty():
        raise FileNotFoundError("OpenCV frontal face cascade could not be loaded.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for i, (x, y, w, h) in enumerate(faces):
            x1, y1 = x + w, y + h
            cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
            cv2.putText(
                frame,
                "face num" + str(i + 1),
                (x - 10, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                3,
            )

        frame = cv2.resize(frame, (1000, 600))
        cv2.imshow(f"Faces: {len(faces)}", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

