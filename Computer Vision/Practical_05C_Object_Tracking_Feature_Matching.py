"""
Practical 05C: Object Tracking using Feature Matching

Requirements:
    python -m pip install opencv-contrib-python numpy

Inputs:
    Place "fd_img.jpg" and "fd.mp4" in the same folder as this script, or edit
    TEMPLATE_IMAGE_PATH and VIDEO_PATH below.
"""

from pathlib import Path

import cv2
import numpy as np


# Original Colab path: /content/fd_img.jpg
TEMPLATE_IMAGE_PATH = Path(__file__).with_name("fd_img.jpg")
# Original Colab path: /content/fd.mp4
VIDEO_PATH = Path(__file__).with_name("fd.mp4")


def main() -> None:
    template = cv2.imread(str(TEMPLATE_IMAGE_PATH), cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Could not read template image: {TEMPLATE_IMAGE_PATH}")

    cap = cv2.VideoCapture(str(VIDEO_PATH))
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {VIDEO_PATH}")

    sift = cv2.SIFT_create()
    kp_template, desc_template = sift.detectAndCompute(template, None)
    if desc_template is None:
        raise RuntimeError("Could not find features in the template image.")

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to read frame.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp_frame, desc_frame = sift.detectAndCompute(gray_frame, None)
        if desc_frame is None:
            cv2.imshow("Object tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

        matches = flann.knnMatch(desc_template, desc_frame, k=2)
        good_points = []
        for pair in matches:
            if len(pair) == 2:
                m, n = pair
                if m.distance < 0.8 * n.distance:
                    good_points.append(m)

        if len(good_points) > 10:
            query_pts = np.float32([kp_template[m.queryIdx].pt for m in good_points]).reshape(-1, 1, 2)
            train_pts = np.float32([kp_frame[m.trainIdx].pt for m in good_points]).reshape(-1, 1, 2)
            matrix, mask = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)
            if matrix is not None:
                h, w = template.shape
                pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                frame = cv2.polylines(frame, [np.int32(dst)], True, (255, 0, 0), 3)
        else:
            print("Not enough good matches found in this frame.")

        cv2.imshow("Object tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

