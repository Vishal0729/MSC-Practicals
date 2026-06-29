"""
Practical 09: Feature Extraction using RANSAC

Requirements:
    python -m pip install opencv-python matplotlib numpy

Inputs:
    Place "cube1.jpg" and "cube2.jpg" in the same folder as this script, or edit
    IMAGE1_PATH and IMAGE2_PATH below.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


# Original Colab path: /content/sample_data/cube1.jpg
IMAGE1_PATH = Path(__file__).with_name("cube1.jpg")
# Original Colab path: /content/sample_data/cube2.jpg
IMAGE2_PATH = Path(__file__).with_name("cube2.jpg")
OUTPUT_PATH = Path(__file__).with_name("output.jpg")


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def main() -> None:
    img1_color = load_image(IMAGE1_PATH)
    img2_color = load_image(IMAGE2_PATH)
    img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)
    height, width = img2.shape

    orb_detector = cv2.ORB_create(5000)
    kp1, d1 = orb_detector.detectAndCompute(img1, None)
    kp2, d2 = orb_detector.detectAndCompute(img2, None)
    if d1 is None or d2 is None:
        raise RuntimeError("Could not find enough ORB features in one or both images.")

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(d1, d2)
    matches = sorted(matches, key=lambda x: x.distance)
    matches = matches[: int(len(matches) * 0.9)]
    if len(matches) < 4:
        raise RuntimeError("At least 4 matches are required for RANSAC homography.")

    p1 = np.zeros((len(matches), 2), dtype=np.float32)
    p2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        p1[i, :] = kp1[match.queryIdx].pt
        p2[i, :] = kp2[match.trainIdx].pt

    homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)
    if homography is None:
        raise RuntimeError("Homography could not be computed.")

    transformed_img = cv2.warpPerspective(img1_color, homography, (width, height))
    cv2.imwrite(str(OUTPUT_PATH), transformed_img)

    fig, axs = plt.subplots(1, 2, figsize=(15, 10))
    axs[0].imshow(cv2.cvtColor(img1_color, cv2.COLOR_BGR2RGB))
    axs[0].set_title("Original Image")
    axs[0].axis("off")
    axs[1].imshow(cv2.cvtColor(transformed_img, cv2.COLOR_BGR2RGB))
    axs[1].set_title("Transformed Image")
    axs[1].axis("off")
    plt.tight_layout()
    plt.show()
    print(f"Saved transformed image to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

