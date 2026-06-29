"""
Practical 06: Pedestrian Detection using Haar Cascade

Requirements:
    python -m pip install opencv-python numpy

Input:
    Place "pedestrainimg.jpg" in the same folder as this script, or edit IMAGE_PATH.

Original PDF path:
    C:/Users/STUDENTS/Desktop/Computer Vision/MSC IT SEM 2 COMPUTER VISION/pedestrainimg.jpg
"""

from pathlib import Path

import cv2


IMAGE_PATH = Path(__file__).with_name("pedestrainimg.jpg")
CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_fullbody.xml"


def main() -> None:
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    pedestrian_cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
    if pedestrian_cascade.empty():
        raise FileNotFoundError(f"Could not load cascade classifier: {CASCADE_PATH}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    pedestrians = pedestrian_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=1, minSize=(5, 5)
    )

    for (x, y, w, h) in pedestrians:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow(f"Pedestrian Detection - {len(pedestrians)} found", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

