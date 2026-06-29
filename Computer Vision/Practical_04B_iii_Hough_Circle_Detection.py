"""
Practical 04B-iii: Hough Circle Detection

Requirements:
    python -m pip install opencv-python matplotlib numpy

Input:
    Place "circle.jpeg" in the same folder as this script, or edit IMAGE_PATH.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


# Original Colab path: /content/circle.jpeg
IMAGE_PATH = Path(__file__).with_name("circle.jpeg")


def main() -> None:
    img = cv2.imread(str(IMAGE_PATH))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        1,
        20,
        param1=100,
        param2=50,
        minRadius=2,
        maxRadius=80,
    )

    circle_count = 0
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        circle_count = len(detected_circles[0])
        for a, b, r in detected_circles[0, :]:
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Circles detected: {circle_count}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

