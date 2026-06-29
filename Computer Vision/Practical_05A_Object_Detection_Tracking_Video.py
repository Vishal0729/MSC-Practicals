"""
Practical 05A: Object Detection and Tracking from Video

Requirements:
    python -m pip install opencv-python numpy

Input:
    Place "highway_video.mp4" in the same folder as this script, or edit
    VIDEO_PATH below.
"""

from pathlib import Path

import cv2


# Original Colab path: /content/highway_video.mp4
VIDEO_PATH = Path(__file__).with_name("highway_video.mp4")


class EuclideanDistTracker:
    def __init__(self) -> None:
        self.center_points = {}
        self.id_count = 0

    def update(self, objects_rect):
        objects_bbs_ids = []

        for rect in objects_rect:
            x, y, w, h = rect
            center_x = (x + x + w) // 2
            center_y = (y + y + h) // 2

            same_object_detected = False
            for object_id, point in self.center_points.items():
                dist = ((center_x - point[0]) ** 2 + (center_y - point[1]) ** 2) ** 0.5
                if dist < 25:
                    self.center_points[object_id] = (center_x, center_y)
                    objects_bbs_ids.append([x, y, w, h, object_id])
                    same_object_detected = True
                    break

            if not same_object_detected:
                self.center_points[self.id_count] = (center_x, center_y)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        new_center_points = {}
        for _, _, _, _, object_id in objects_bbs_ids:
            new_center_points[object_id] = self.center_points[object_id]
        self.center_points = new_center_points.copy()
        return objects_bbs_ids


def select_roi(frame):
    height, width = frame.shape[:2]
    x1, y1, x2, y2 = 500, 340, 800, 720
    if width < x2 or height < y2:
        return frame
    return frame[y1:y2, x1:x2]


def main() -> None:
    tracker = EuclideanDistTracker()
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {VIDEO_PATH}")

    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or cannot read the frame.")
            break

        roi = select_roi(frame)
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        boxes_ids = tracker.update(detections)
        for x, y, w, h, object_id in boxes_ids:
            cv2.putText(roi, str(object_id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("ROI", roi)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        if cv2.waitKey(30) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

