"""
Practical 04C: Pedestrian Detection

Requirements:
    python -m pip install opencv-python numpy

Input:
    Place "people_walking.jpg" in the same folder as this script, or edit IMAGE_PATH.
"""

from pathlib import Path

import cv2


# Original Colab path: /content/people_walking.jpg
IMAGE_PATH = Path(__file__).with_name("people_walking.jpg")


def resize_to_width(image, width: int):
    if image.shape[1] <= width:
        return image
    ratio = width / image.shape[1]
    height = int(image.shape[0] * ratio)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)


def main() -> None:
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    image = resize_to_width(image, 400)
    regions, _ = hog.detectMultiScale(
        image, winStride=(4, 4), padding=(4, 4), scale=1.05
    )
    for (x, y, w, h) in regions:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow(f"Pedestrians detected: {len(regions)}", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

