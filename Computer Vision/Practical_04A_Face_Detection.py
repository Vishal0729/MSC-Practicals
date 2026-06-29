"""
Practical 04A: Face Detection

Requirements:
    python -m pip install opencv-python matplotlib numpy

Input:
    Place "cricket.webp" in the same folder as this script, or edit IMAGE_PATH.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt


# Original Colab path: /content/cricket.webp
IMAGE_PATH = Path(__file__).with_name("cricket.webp")
# Original Colab path: /content/haarcascade_frontalface_default.xml
CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"


def main() -> None:
    img = cv2.imread(str(IMAGE_PATH))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(str(CASCADE_PATH))
    if face_classifier.empty():
        raise FileNotFoundError(f"Could not load cascade classifier: {CASCADE_PATH}")

    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(12, 7))
    plt.imshow(img_rgb)
    plt.title(f"Faces detected: {len(faces)}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

