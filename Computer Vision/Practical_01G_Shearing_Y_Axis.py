"""
Practical 01G: Shearing on Y-axis

Requirements:
    python -m pip install opencv-python matplotlib numpy

Input:
    Place "cherry blossom 1.jpg" in the same folder as this script, or edit
    IMAGE_PATH below.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


# Original Colab path: /content/cherry blossom 1.jpg
IMAGE_PATH = Path(__file__).with_name("cherry blossom 1.jpg")


def load_image_rgb(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def main() -> None:
    img_rgb = load_image_rgb(IMAGE_PATH)
    rows, cols, _ = img_rgb.shape

    matrix = np.float32([[1, 0, 0], [0.5, 1, 0], [0, 0, 1]])
    output = cv2.warpPerspective(img_rgb, matrix, (int(cols * 1.5), int(rows * 1.5)))

    plt.subplot(121)
    plt.imshow(img_rgb)
    plt.title("Original Image")
    plt.axis("off")
    plt.subplot(122)
    plt.imshow(output)
    plt.title("Output Image")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

