"""
Practical 07: Feature Extraction using RANSAC

Requirements:
    python -m pip install matplotlib numpy scikit-learn

Input:
    No external file is required. This program generates noisy sample data and
    fits a robust line using RANSAC.
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import RANSACRegressor


def main() -> None:
    np.random.seed(0)
    x = np.random.uniform(0, 10, 100)
    y = 2 * x + 1 + np.random.normal(0, 1, 100)

    outlier_indices = np.random.choice(100, 20, replace=False)
    y[outlier_indices] += 10 * np.random.normal(0, 1, 20)

    data = np.vstack((x, y)).T
    ransac = RANSACRegressor(random_state=0)
    ransac.fit(data[:, 0].reshape(-1, 1), data[:, 1])

    inlier_mask = ransac.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)
    line_slope = ransac.estimator_.coef_[0]
    line_intercept = ransac.estimator_.intercept_

    x_line = np.linspace(x.min(), x.max(), 200)
    y_line = line_slope * x_line + line_intercept

    plt.scatter(data[inlier_mask][:, 0], data[inlier_mask][:, 1], c="b", label="Inliers")
    plt.scatter(data[outlier_mask][:, 0], data[outlier_mask][:, 1], c="r", label="Outliers")
    plt.plot(x_line, y_line, color="g", label="RANSAC line")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

