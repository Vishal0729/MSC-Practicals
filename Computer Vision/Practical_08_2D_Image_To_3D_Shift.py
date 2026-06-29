"""
Practical 08: Construct 3D Model from Images

Requirements:
    python -m pip install pillow matplotlib numpy

Inputs:
    Place "cube1.jpg" and "cube2.jpg" in the same folder as this script, or edit
    IMAGE_PATH and DEPTH_IMAGE_PATH below. The second image is used as a depth map.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# Original Colab path: /content/sample_data/cube1.jpg
IMAGE_PATH = Path(__file__).with_name("cube1.jpg")
# Original Colab path: /content/sample_data/cube2.jpg
DEPTH_IMAGE_PATH = Path(__file__).with_name("cube2.jpg")


def shift_image(img: Image.Image, depth_img: Image.Image, shift_amount: int = 10) -> Image.Image:
    img = img.convert("RGBA")
    data = np.array(img)

    depth_img = depth_img.convert("L").resize(img.size)
    depth_data = np.array(depth_img)
    deltas = ((depth_data / 255.0) * float(shift_amount)).astype(int)
    shifted_data = np.zeros_like(data)
    height, width, _ = data.shape

    for y, row in enumerate(deltas):
        for x, dx in enumerate(row):
            if 0 <= x + dx < width:
                shifted_data[y, x + dx] = data[y, x]

    return Image.fromarray(shifted_data.astype(np.uint8))


def main() -> None:
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")
    if not DEPTH_IMAGE_PATH.exists():
        raise FileNotFoundError(f"Could not read depth image: {DEPTH_IMAGE_PATH}")

    img = Image.open(IMAGE_PATH)
    depth_img = Image.open(DEPTH_IMAGE_PATH)
    shifted_img = shift_image(img, depth_img, shift_amount=10)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].imshow(img)
    axs[0].set_title("Original Image")
    axs[0].axis("off")
    axs[1].imshow(shifted_img)
    axs[1].set_title("Shifted Image")
    axs[1].axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

