"""
Practical 05: TensorFlow Object Detection

Requirements:
    python -m pip install opencv-python numpy tensorflow

Inputs:
    Place these files/folders in the same folder as this script, or edit the
    paths below:
    - IMG.jpg
    - mscoco_label_map.pbtxt
    - ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb

Original PDF paths:
    C:/Users/STUDENTS/Desktop/Computer Vision/MSC IT SEM 2 COMPUTER VISION/IMG.jpg
    C:/Users/STUDENTS/Desktop/Computer Vision/MSC IT SEM 2 COMPUTER VISION/mscoco_label_map.pbtxt
"""

from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


SCRIPT_DIR = Path(__file__).resolve().parent
IMAGE_PATH = SCRIPT_DIR / "IMG.jpg"
MODEL_NAME = "ssd_mobilenet_v2_coco_2018_03_29"
FROZEN_GRAPH_PATH = SCRIPT_DIR / MODEL_NAME / "frozen_inference_graph.pb"
LABEL_MAP_PATH = SCRIPT_DIR / "mscoco_label_map.pbtxt"
CONFIDENCE_THRESHOLD = 0.5


def load_label_map(path: Path) -> dict[int, str]:
    if not path.exists():
        raise FileNotFoundError(f"Could not find label map: {path}")

    labels = {}
    current_id = None
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if line.startswith("id:"):
            current_id = int(line.split(":", 1)[1].strip())
        elif "display_name:" in line or "name:" in line:
            if current_id is not None:
                name = line.split(":", 1)[1].strip().strip('"').strip("'")
                labels[current_id] = name
                current_id = None
    return labels


def load_detection_graph(path: Path) -> tf.Graph:
    if not path.exists():
        raise FileNotFoundError(f"Could not find frozen graph: {path}")

    graph = tf.Graph()
    with graph.as_default():
        graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(str(path), "rb") as fid:
            graph_def.ParseFromString(fid.read())
        tf.import_graph_def(graph_def, name="")
    return graph


def detect_objects(image: np.ndarray, graph: tf.Graph, category_index: dict[int, str]) -> np.ndarray:
    output = image.copy()
    with graph.as_default():
        with tf.compat.v1.Session(graph=graph) as sess:
            image_expanded = np.expand_dims(image, axis=0)
            image_tensor = graph.get_tensor_by_name("image_tensor:0")
            boxes_tensor = graph.get_tensor_by_name("detection_boxes:0")
            scores_tensor = graph.get_tensor_by_name("detection_scores:0")
            classes_tensor = graph.get_tensor_by_name("detection_classes:0")
            detections_tensor = graph.get_tensor_by_name("num_detections:0")

            boxes, scores, classes, _ = sess.run(
                [boxes_tensor, scores_tensor, classes_tensor, detections_tensor],
                feed_dict={image_tensor: image_expanded},
            )

    height, width = output.shape[:2]
    for i, score in enumerate(scores[0]):
        if score <= CONFIDENCE_THRESHOLD:
            continue
        class_id = int(classes[0][i])
        class_name = category_index.get(class_id, f"class {class_id}")
        ymin, xmin, ymax, xmax = boxes[0][i]
        left, right = int(xmin * width), int(xmax * width)
        top, bottom = int(ymin * height), int(ymax * height)
        cv2.rectangle(output, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(
            output,
            f"{class_name}: {float(score):.2f}",
            (left, max(top - 5, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
    return output


def main() -> None:
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    category_index = load_label_map(LABEL_MAP_PATH)
    detection_graph = load_detection_graph(FROZEN_GRAPH_PATH)
    output_image = detect_objects(image, detection_graph, category_index)

    cv2.imshow("Object Detection", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

