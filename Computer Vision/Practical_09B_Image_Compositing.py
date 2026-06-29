"""
Practical 09B: Image Compositing

Requirements:
    python -m pip install opencv-python numpy

Inputs:
    Place these files in the same folder as this script, or edit the paths below:
    - foreground.jpg
    - background.jpg
    - trimap.png

Original PDF path used model.jpg for all inputs:
    C:/Users/STUDENTS/Desktop/Computer Vision/MSC IT SEM 2 COMPUTER VISION/model.jpg
"""

from pathlib import Path

import cv2
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
FOREGROUND_PATH = SCRIPT_DIR / "foreground.jpg"
BACKGROUND_PATH = SCRIPT_DIR / "background.jpg"
TRIMAP_PATH = SCRIPT_DIR / "trimap.png"
OUTPUT_PATH = SCRIPT_DIR / "composited_image.png"


def load_color_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def load_trimap(path: Path) -> np.ndarray:
    trimap = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if trimap is None:
        raise FileNotFoundError(f"Could not read trimap: {path}")
    return trimap


def estimate_alpha(trimap: np.ndarray) -> np.ndarray:
    alpha = np.zeros_like(trimap, dtype=np.float32)
    alpha[trimap >= 250] = 1.0
    alpha[trimap <= 5] = 0.0

    unknown = (trimap > 5) & (trimap < 250)
    alpha[unknown] = trimap[unknown].astype(np.float32) / 255.0
    return np.clip(alpha, 0.0, 1.0)


def composite_foreground_background(
    foreground: np.ndarray, background: np.ndarray, alpha: np.ndarray
) -> np.ndarray:
    background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))
    if alpha.shape[:2] != foreground.shape[:2]:
        alpha = cv2.resize(alpha, (foreground.shape[1], foreground.shape[0]))

    foreground_float = foreground.astype(np.float32) / 255.0
    background_float = background.astype(np.float32) / 255.0
    alpha_3channel = np.dstack([alpha, alpha, alpha])
    composited = alpha_3channel * foreground_float + (1.0 - alpha_3channel) * background_float
    return (np.clip(composited, 0.0, 1.0) * 255).astype(np.uint8)


def main() -> None:
    foreground = load_color_image(FOREGROUND_PATH)
    background = load_color_image(BACKGROUND_PATH)
    trimap = load_trimap(TRIMAP_PATH)

    alpha = estimate_alpha(trimap)
    composited_image = composite_foreground_background(foreground, background, alpha)

    cv2.imwrite(str(OUTPUT_PATH), composited_image)
    cv2.imshow("Composited Image", composited_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"Saved composited image to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

