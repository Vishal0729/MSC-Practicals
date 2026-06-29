"""
Practical 04B-ii: Line Detection

Requirements:
    python -m pip install opencv-python matplotlib numpy

Input:
    Place "lines.png" in the same folder as this script, or edit IMAGE_PATH.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


# Original Colab path: /content/lines.png
IMAGE_PATH = Path(__file__).with_name("lines.png")


def main() -> None:
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    line_list = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges,
        rho=2,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=20,
        maxLineGap=5,
    )

    if lines is not None:
        for points in lines:
            x1, y1, x2, y2 = points[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            line_list.append([(x1, y1), (x2, y2)])

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f"Lines detected: {len(line_list)}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

