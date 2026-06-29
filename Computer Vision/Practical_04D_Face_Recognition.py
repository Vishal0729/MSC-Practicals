"""
Practical 04D: Face Recognition Label

Requirements:
    python -m pip install opencv-python numpy

Input:
    Place "image.jpg" in the same folder as this script, or edit IMAGE_PATH.

Note:
    The PDF labels a detected face with text. This is face detection plus a
    label overlay, not a trained face-recognition model.
"""

from pathlib import Path

import cv2


# Original Colab path: /content/image.jpg
IMAGE_PATH = Path(__file__).with_name("image.jpg")
FACE_LABEL = "I am Manasi Singh"


def main() -> None:
    img = cv2.imread(str(IMAGE_PATH))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
    )
    if face_cascade.empty():
        raise FileNotFoundError("OpenCV frontal face cascade could not be loaded.")

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 1
    text_size, _ = cv2.getTextSize(FACE_LABEL, font, font_scale, font_thickness)
    text_x = 20
    text_y = 30 + text_size[1]
    cv2.putText(
        img,
        FACE_LABEL,
        (text_x, text_y),
        font,
        font_scale,
        (0, 0, 0),
        font_thickness,
        cv2.LINE_AA,
    )

    scale_percent = 20
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imshow(f"Faces detected: {len(faces)}", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

