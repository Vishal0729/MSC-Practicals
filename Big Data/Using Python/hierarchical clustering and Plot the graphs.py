# Required libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# ===== Step 1: Load the Dataset =====
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data"
# Column names as per UCI documentation
columns = ['Class', 'Alcohol', 'Malic_Acid', 'Ash', 'Alcalinity_of_Ash',
           'Magnesium', 'Total_Phenols', 'Flavanoids', 'Nonflavanoid_Phenols',
           'Proanthocyanins', 'Color_Intensity', 'Hue', 'OD280_OD315', 'Proline']
df = pd.read_csv(url, names=columns)

# --- If file is downloaded locally, use this instead: ---
# df = pd.read_csv("wine.data", names=columns)
# --------------------------------------------------------

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nClass distribution (actual labels for reference):")
print(df['Class'].value_counts().sort_index())

# ===== Step 2: Prepare Features (exclude Class column) =====
X = df.drop(columns=['Class'])
actual_labels = df['Class']

# ===== Step 3: Feature Scaling =====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("\nFeatures scaled using StandardScaler")

# ===== Step 4: Perform Hierarchical Clustering (Agglomerative) =====
# Compute linkage matrix using Ward's method
linkage_ward = linkage(X_scaled, method='ward')
linkage_complete = linkage(X_scaled, method='complete')
linkage_average = linkage(X_scaled, method='average')
print("\nLinkage matrices computed (Ward, Complete, Average)")

# ===== Step 5: Plot Dendrogram (Ward's Method) =====
plt.figure(figsize=(14, 7))
dendrogram(linkage_ward, truncate_mode='lastp', p=30,
           leaf_rotation=90, leaf_font_size=10,
           show_contracted=True)
plt.xlabel("Sample Index / Cluster Size")
plt.ylabel("Distance")
plt.title("Dendrogram - Ward's Method (Wine Dataset)")
plt.axhline(y=25, color='r', linestyle='--', label='Cut at 3 clusters')
plt.legend()
plt.tight_layout()
plt.savefig("dendrogram_ward.png")
plt.show()

# ===== Step 6: Plot Dendrograms for All Methods =====
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Ward
axes[0].set_title("Ward's Method")
dendrogram(linkage_ward, ax=axes[0], truncate_mode='lastp', p=20,
           leaf_rotation=90, leaf_font_size=8)
axes[0].axhline(y=25, color='r', linestyle='--')

# Complete
axes[1].set_title("Complete Linkage")
dendrogram(linkage_complete, ax=axes[1], truncate_mode='lastp', p=20,
           leaf_rotation=90, leaf_font_size=8)
axes[1].axhline(y=8, color='r', linestyle='--')

# Average
axes[2].set_title("Average Linkage")
dendrogram(linkage_average, ax=axes[2], truncate_mode='lastp', p=20,
           leaf_rotation=90, leaf_font_size=8)
axes[2].axhline(y=6, color='r', linestyle='--')

plt.suptitle("Comparison of Linkage Methods", fontsize=14)
plt.tight_layout()
plt.savefig("dendrograms_comparison.png")
plt.show()

# ===== Step 7: Cut Dendrogram to Form Clusters =====
n_clusters = 3
clusters = fcluster(linkage_ward, t=n_clusters, criterion='maxclust')
df['Cluster'] = clusters
print(f"\nClusters formed (K={n_clusters}):")
print(f"\nCluster distribution:")
print(pd.Series(clusters).value_counts().sort_index())

# ===== Step 8: Evaluate Clustering =====
silhouette_avg = silhouette_score(X_scaled, clusters)
print(f"\nSilhouette Score: {silhouette_avg:.4f}")

# Compare with actual labels
from sklearn.metrics import adjusted_rand_score
ari = adjusted_rand_score(actual_labels, clusters)
print(f"Adjusted Rand Index (vs actual): {ari:.4f}")

# ===== Step 9: Plot Clusters (2D using first 2 features) =====
plt.figure(figsize=(10, 7))
colors = ['red', 'blue', 'green']

for i in range(1, n_clusters + 1):
    cluster_data = X_scaled[clusters == i]
    plt.scatter(cluster_data[:, 0], cluster_data[:, 1],
                s=80, c=colors[i-1], label=f'Cluster {i}',
                alpha=0.7, edgecolors='k')

plt.xlabel("Alcohol (Scaled)")
plt.ylabel("Malic Acid (Scaled)")
plt.title("Hierarchical Clustering - Wine Dataset (Ward's Method)")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("hierarchical_clusters_2d.png")
plt.show()

# ===== Step 10: Plot Clusters using PCA (Better Visualization) =====
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 7))
for i in range(1, n_clusters + 1):
    mask = clusters == i
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1],
                s=80, c=colors[i-1], label=f'Cluster {i}',
                alpha=0.7, edgecolors='k')

plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
plt.title("Hierarchical Clustering - PCA Projection (Wine Dataset)")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("hierarchical_clusters_pca.png")
plt.show()

# ===== Step 11: Cluster Summary =====
print(f"\n{'='*60}")
print("  CLUSTER SUMMARY")
print(f"{'='*60}")
for i in range(1, n_clusters + 1):
    cluster_data = df[df['Cluster'] == i]
    print(f"\n  Cluster {i} ({len(cluster_data)} samples):")
    print(f"    Avg Alcohol:         {cluster_data['Alcohol'].mean():.2f}")
    print(f"    Avg Flavanoids:      {cluster_data['Flavanoids'].mean():.2f}")
    print(f"    Avg Color Intensity: {cluster_data['Color_Intensity'].mean():.2f}")
    print(f"    Avg Proline:         {cluster_data['Proline'].mean():.2f}")