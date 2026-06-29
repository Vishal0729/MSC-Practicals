"""
Practical 01: Point-Based Geometric Transformation

Requirements:
    python -m pip install matplotlib numpy

Input:
    No external image file is required. This program transforms sample 2D points.
"""

import matplotlib.pyplot as plt
import numpy as np


def to_homogeneous(points: np.ndarray) -> np.ndarray:
    return np.hstack([points, np.ones((points.shape[0], 1))])


def apply_transform(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    transformed = matrix @ to_homogeneous(points).T
    return transformed.T[:, :2]


def main() -> None:
    points = np.array([[1, 1], [2, 2], [3, 1]], dtype=float)

    translation_matrix = np.array([[1, 0, 2], [0, 1, 3], [0, 0, 1]], dtype=float)
    theta = np.pi / 4
    rotation_matrix = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ],
        dtype=float,
    )
    scaling_matrix = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]], dtype=float)

    translated_points = apply_transform(points, translation_matrix)
    rotated_points = apply_transform(points, rotation_matrix)
    scaled_points = apply_transform(points, scaling_matrix)

    transformations = [
        ("Translation", translated_points, "Translated"),
        ("Rotation", rotated_points, "Rotated"),
        ("Scaling", scaled_points, "Scaled"),
    ]

    plt.figure(figsize=(10, 5))
    for index, (title, transformed_points, label) in enumerate(transformations, start=1):
        plt.subplot(1, 3, index)
        plt.title(title)
        plt.plot(points[:, 0], points[:, 1], "bo", label="Original")
        plt.plot(transformed_points[:, 0], transformed_points[:, 1], "r+", label=label)
        plt.axis("equal")
        plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

