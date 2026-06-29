"""
Practical 02: Image Stitching

Requirements:
    python -m pip install opencv-contrib-python matplotlib numpy

Inputs:
    Place both images in the same folder as this script, or edit IMAGE1_PATH and
    IMAGE2_PATH below.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


# Original Colab path: /content/cherry blossom 1.jpg
IMAGE1_PATH = Path(__file__).with_name("cherry blossom 1.jpg")
# Original Colab path: /content/cherry blossom 2.jpg
IMAGE2_PATH = Path(__file__).with_name("cherry blossom 2.jpg")
OUTPUT_PATH = Path(__file__).with_name("resultant_stitched_panorama.jpg")


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def main() -> None:
    image1 = load_image(IMAGE1_PATH)
    image2 = load_image(IMAGE2_PATH)
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)
    if descriptors1 is None or descriptors2 is None:
        raise RuntimeError("Could not find enough features in one or both images.")

    matcher = cv2.BFMatcher()
    raw_matches = matcher.knnMatch(descriptors1, descriptors2, k=2)
    good_matches = [m for m, n in raw_matches if m.distance < 0.5 * n.distance]
    if len(good_matches) < 4:
        raise RuntimeError("At least 4 good matches are required for homography.")

    src = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    homography, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    if homography is None:
        raise RuntimeError("Homography could not be computed.")

    height = max(image1.shape[0], image2.shape[0])
    width = image1.shape[1] + image2.shape[1]
    result = cv2.warpPerspective(image1, homography, (width, height))
    result[0 : image2.shape[0], 0 : image2.shape[1]] = image2

    cv2.imwrite(str(OUTPUT_PATH), result)
    plt.figure(figsize=(10, 5))
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Resultant Stitched Panorama")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    print(f"Saved stitched image to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

