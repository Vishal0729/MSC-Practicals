"""
Practical 03: Camera Calibration

Requirements:
    python -m pip install opencv-python matplotlib numpy

Inputs:
    Put chessboard calibration images in the same folder as this script and edit
    CALIBRATION_IMAGE_GLOB if needed. A 7 x 6 inner-corner board is expected.
"""

from pathlib import Path
import glob

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
# Original Colab path: /content/chess.jpg
CALIBRATION_IMAGE_GLOB = str(SCRIPT_DIR / "chess*.jpg")
# Original Colab path: /content/left08.jpg
UNDISTORT_IMAGE_PATH = SCRIPT_DIR / "left08.jpg"
OUTPUT_PATH = SCRIPT_DIR / "calibresult.png"
CHESSBOARD_SIZE = (7, 6)


def main() -> None:
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0 : CHESSBOARD_SIZE[0], 0 : CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []
    last_gray = None

    images = sorted(glob.glob(CALIBRATION_IMAGE_GLOB))
    if not images:
        raise FileNotFoundError(f"No calibration images matched: {CALIBRATION_IMAGE_GLOB}")

    for fname in images:
        img = cv.imread(fname)
        if img is None:
            print(f"Failed to load image {fname}")
            continue

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, CHESSBOARD_SIZE, None)
        if not ret:
            print(f"Chessboard corners not found in image {fname}")
            continue

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        last_gray = gray

        cv.drawChessboardCorners(img, CHESSBOARD_SIZE, corners2, ret)
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        plt.title(Path(fname).name)
        plt.axis("off")
        plt.show()

    if not objpoints or last_gray is None:
        raise RuntimeError("No usable chessboard corners were found; calibration cannot run.")

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
        objpoints, imgpoints, last_gray.shape[::-1], None, None
    )
    print("Camera matrix:")
    print(mtx)
    print("Distortion coefficients:")
    print(dist)
    print("Rotation vectors:")
    print(rvecs)
    print("Translation vectors:")
    print(tvecs)

    img = cv.imread(str(UNDISTORT_IMAGE_PATH))
    if img is None:
        raise FileNotFoundError(f"Could not read image for undistortion: {UNDISTORT_IMAGE_PATH}")

    h, w = img.shape[:2]
    new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistorted = cv.undistort(img, mtx, dist, None, new_camera_mtx)
    x, y, roi_w, roi_h = roi
    if roi_w > 0 and roi_h > 0:
        undistorted = undistorted[y : y + roi_h, x : x + roi_w]

    cv.imwrite(str(OUTPUT_PATH), undistorted)
    plt.imshow(cv.cvtColor(undistorted, cv.COLOR_BGR2RGB))
    plt.title("Undistorted Image")
    plt.axis("off")
    plt.show()
    print(f"Saved undistorted image to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

