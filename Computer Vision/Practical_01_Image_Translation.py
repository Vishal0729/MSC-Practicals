"""
Practical 01: Image Translation

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

    matrix = np.float32([[1, 0, 100], [0, 1, 50]])
    translated_image = cv2.warpAffine(img_rgb, matrix, (cols, rows))

    fig, axs = plt.subplots(1, 2, figsize=(7, 4))
    axs[0].imshow(img_rgb)
    axs[0].set_title("Original image")
    axs[0].axis("off")
    axs[1].imshow(translated_image)
    axs[1].set_title("Translated image")
    axs[1].axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

