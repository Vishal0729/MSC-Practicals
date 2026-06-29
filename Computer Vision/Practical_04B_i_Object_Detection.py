"""
Practical 04B-i: Object Detection with a Haar Cascade

Requirements:
    python -m pip install opencv-python matplotlib numpy

Input:
    Place "images.jfif" in the same folder as this script, or edit IMAGE_PATH.
    The PDF uses a cat-face cascade; OpenCV usually ships that cascade file.
"""

from pathlib import Path

import cv2
from matplotlib import pyplot as plt


# Original Colab path: /content/images.jfif
IMAGE_PATH = Path(__file__).with_name("images.jfif")
# Original Colab path: /content/haarcascade_frontalcatface.xml
CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalcatface.xml"


def main() -> None:
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
    if cascade.empty():
        raise FileNotFoundError(f"Could not load cascade classifier: {CASCADE_PATH}")

    detections = cascade.detectMultiScale(image_gray, minSize=(30, 30))
    for (x, y, width, height) in detections:
        cv2.rectangle(image_rgb, (x, y), (x + width, y + height), (0, 255, 0), 9)

    plt.imshow(image_rgb)
    plt.title(f"Detections: {len(detections)}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

