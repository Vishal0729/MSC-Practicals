from time import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble, discriminant_analysis, random_projection)

warnings.filterwarnings("ignore")

# Load digit dataset (proxy for container number images)
digits = datasets.load_digits(n_class=6)
X = digits.data
y = digits.target

n_samples, n_features = X.shape
n_neighbors = 30

# Utility function to plot embeddings
def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111)

    for i in range(X.shape[0]):
        plt.text(
            X[i, 0],
            X[i, 1],
            str(y[i]),
            color=plt.cm.Set1(y[i] / 10.),
            fontdict={'weight': 'bold', 'size': 9}
        )

    if hasattr(offsetbox, "AnnotationBbox"):
        shown_images = np.array([[1., 1.]])
        for i in range(digits.data.shape[0]):
            dist = np.sum((X[i] - shown_images) ** 2, 1)
            if np.min(dist) < 4e-3:
                continue
            shown_images = np.r_[shown_images, [X[i]]]
            imagebox = offsetbox.AnnotationBbox(
                offsetbox.OffsetImage(digits.images[i], cmap=plt.cm.gray_r),
                X[i]
            )
            ax.add_artist(imagebox)

    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)

# Show sample digit images
n_img_per_row = 20
img = np.zeros((10 * n_img_per_row, 10 * n_img_per_row))

for i in range(n_img_per_row):
    ix = 10 * i + 1
    for j in range(n_img_per_row):
        iy = 10 * j + 1
        img[ix:ix + 8, iy:iy + 8] = X[i * n_img_per_row + j].reshape((8, 8))

plt.figure(figsize=(10, 10))
plt.imshow(img, cmap=plt.cm.binary)
plt.xticks([])
plt.yticks([])
plt.title("A selection from the 64-dimensional digits dataset")

# Random Projection
print("Computing random projection")
rp = random_projection.SparseRandomProjection(n_components=2, random_state=42)
X_rp = rp.fit_transform(X)
plot_embedding(X_rp, "Random Projection")

# PCA
print("Computing PCA projection")
t0 = time()
X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X)
plot_embedding(X_pca, "PCA Projection (time %.2fs)" % (time() - t0))

# Linear Discriminant Analysis
print("Computing Linear Discriminant Analysis projection")
X2 = X.copy()
X2.flat[::X.shape[1] + 1] += 0.01  # make invertible
t0 = time()
X_lda = discriminant_analysis.LinearDiscriminantAnalysis(
    n_components=2
).fit_transform(X2, y)
plot_embedding(X_lda, "LDA Projection (time %.2fs)" % (time() - t0))

# Isomap
print("Computing Isomap embedding")
t0 = time()
X_iso = manifold.Isomap(
    n_neighbors=5,
    n_components=2
).fit_transform(X)
plot_embedding(X_iso, "Isomap (time %.2fs)" % (time() - t0))

# Standard LLE
print("Computing LLE embedding")
clf = manifold.LocallyLinearEmbedding(
    n_neighbors=5,
    n_components=2,
    method="standard"
)
t0 = time()
X_lle = clf.fit_transform(X)
plot_embedding(X_lle, "LLE (time %.2fs)" % (time() - t0))

# Modified LLE
print("Computing modified LLE embedding")
clf = manifold.LocallyLinearEmbedding(
    n_neighbors=5,
    n_components=2,
    method="modified"
)
t0 = time()
X_mlle = clf.fit_transform(X)
plot_embedding(X_mlle, "Modified LLE (time %.2fs)" % (time() - t0))

# Hessian LLE (FIXED)
print("Computing Hessian LLE embedding")
clf = manifold.LocallyLinearEmbedding(
    n_neighbors=n_neighbors,
    n_components=2,
    method="hessian",
    eigen_solver="dense"   # CRITICAL FIX
)
t0 = time()
X_hlle = clf.fit_transform(X)
plot_embedding(X_hlle, "Hessian LLE (time %.2fs)" % (time() - t0))

# LTSA
print("Computing LTSA embedding")
clf = manifold.LocallyLinearEmbedding(
    n_neighbors=n_neighbors,
    n_components=2,
    method="ltsa"
)
t0 = time()
X_ltsa = clf.fit_transform(X)
plot_embedding(X_ltsa, "LTSA (time %.2fs)" % (time() - t0))

# MDS
print("Computing MDS embedding")
clf = manifold.MDS(n_components=2, n_init=1, max_iter=100)
t0 = time()
X_mds = clf.fit_transform(X)
plot_embedding(X_mds, "MDS (time %.2fs)" % (time() - t0))

# Random Trees Embedding
print("Computing Random Trees embedding")
hasher = ensemble.RandomTreesEmbedding(
    n_estimators=200,
    random_state=0,
    max_depth=5
)
t0 = time()
X_transformed = hasher.fit_transform(X)
X_reduced = decomposition.TruncatedSVD(n_components=2).fit_transform(X_transformed)
plot_embedding(X_reduced, "Random Trees (time %.2fs)" % (time() - t0))

# Spectral Embedding
print("Computing Spectral embedding")
embedder = manifold.SpectralEmbedding(
    n_components=2,
    random_state=0,
    eigen_solver="arpack"
)
t0 = time()
X_se = embedder.fit_transform(X)
plot_embedding(X_se, "Spectral Embedding (time %.2fs)" % (time() - t0))

# t-SNE
print("Computing t-SNE embedding")
tsne = manifold.TSNE(
    n_components=2,
    init="pca",
    random_state=0,
)
t0 = time()
X_tsne = tsne.fit_transform(X)
plot_embedding(X_tsne, "t-SNE (time %.2fs)" % (time() - t0))

plt.show()
print("Done.")