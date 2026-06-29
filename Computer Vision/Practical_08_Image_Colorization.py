"""
Practical 08: Colorization of an Image

Requirements:
    python -m pip install opencv-python numpy

Input:
    Place "grayimg.jpeg" in the same folder as this script, or edit IMAGE_PATH.

Original PDF path:
    C:/Users/STUDENTS/Desktop/Computer Vision/MSC IT SEM 2 COMPUTER VISION/grayimg.jpeg
"""

from pathlib import Path

import cv2
import numpy as np


IMAGE_PATH = Path(__file__).with_name("grayimg.jpeg")


def build_color_lookup_table() -> np.ndarray:
    color_lookup_table = np.zeros((256, 1, 3), dtype=np.uint8)
    for i in range(256):
        color_lookup_table[i, 0, 0] = i
        color_lookup_table[i, 0, 1] = 127
        color_lookup_table[i, 0, 2] = 255 - i
    return color_lookup_table


def main() -> None:
    gray_image = cv2.imread(str(IMAGE_PATH), cv2.IMREAD_GRAYSCALE)
    if gray_image is None:
        raise FileNotFoundError(f"Could not read grayscale image: {IMAGE_PATH}")

    color_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    colorized_image = cv2.LUT(color_image, build_color_lookup_table())

    cv2.imshow("Grayscale Image", gray_image)
    cv2.imshow("Colorized Image", colorized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

