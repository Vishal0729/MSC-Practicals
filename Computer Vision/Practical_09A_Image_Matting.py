"""
Practical 09A: Image Matting

Requirements:
    python -m pip install opencv-python numpy

Input:
    Place "trimap.png" in the same folder as this script, or edit TRIMAP_PATH.

Original PDF path:
    C:/Users/STUDENTS/Desktop/Computer Vision/MSC IT SEM 2 COMPUTER VISION/model.jpg
"""

from pathlib import Path

import cv2
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
TRIMAP_PATH = SCRIPT_DIR / "trimap.png"
ALPHA_OUTPUT_PATH = SCRIPT_DIR / "alpha_matte.png"


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


def main() -> None:
    trimap = load_trimap(TRIMAP_PATH)
    alpha = estimate_alpha(trimap)

    alpha_image = (alpha * 255).astype(np.uint8)
    cv2.imwrite(str(ALPHA_OUTPUT_PATH), alpha_image)
    cv2.imshow("Alpha Matte", alpha_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"Saved alpha matte to: {ALPHA_OUTPUT_PATH}")


if __name__ == "__main__":
    main()

