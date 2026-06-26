# Required libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ===== Step 1: Load the Dataset =====
url = "https://raw.githubusercontent.com/SteffiPeTaworworworworworworworworworworworwor/machineLearning/master/Mall_Customers.csv"
# Alternative URL that works:
url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/Mall_Customers.csv"
df = pd.read_csv(url)

# --- If file is downloaded locally, use this instead: ---
# df = pd.read_csv("Mall_Customers.csv")
# --------------------------------------------------------

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset Info:")
print(df.describe())

# ===== Step 2: Select Features for Clustering =====
# Using Annual Income and Spending Score
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]
print("\nFeatures selected: Annual Income & Spending Score")
print(X.head())

# ===== Step 3: Feature Scaling =====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===== Step 4: Find Optimal K using Elbow Method =====
wcss = []  # Within-Cluster Sum of Squares
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plot Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(k_range, wcss, 'bo-', linewidth=2, markersize=8)
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS (Within-Cluster Sum of Squares)")
plt.title("Elbow Method - Optimal K")
plt.grid(True)
plt.tight_layout()
plt.savefig("elbow_method.png")
plt.show()

print("\nWCSS values:")
for k, w in zip(k_range, wcss):
    print(f"  K={k:<3} WCSS={w:.2f}")
print("\nOptimal K = 5 (from elbow point)")

# ===== Step 5: Apply K-Means with Optimal K =====
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels to dataframe
df['Cluster'] = clusters
print(f"\nK-Means applied with K={optimal_k}")
print("\nCluster distribution:")
print(df['Cluster'].value_counts().sort_index())

# ===== Step 6: Cluster Centers =====
# Inverse transform to get original scale
centers = scaler.inverse_transform(kmeans.cluster_centers_)
print("\nCluster Centers (Original Scale):")
print(f"{'Cluster':<10} {'Annual Income (k$)':<22} {'Spending Score':<15}")
print(f"{'-'*10} {'-'*22} {'-'*15}")
for i, center in enumerate(centers):
    print(f"{i:<10} {center[0]:<22.2f} {center[1]:<15.2f}")

# ===== Step 7: Plot Clusters =====
plt.figure(figsize=(10, 7))
colors = ['red', 'blue', 'green', 'orange', 'purple']
labels = ['Low Income/Low Spend', 'High Income/High Spend', 
          'High Income/Low Spend', 'Low Income/High Spend', 'Medium']

for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    plt.scatter(cluster_data['Annual Income (k$)'], 
                cluster_data['Spending Score (1-100)'],
                s=80, c=colors[i], label=f'Cluster {i}', alpha=0.7, edgecolors='k')

# Plot centroids
plt.scatter(centers[:, 0], centers[:, 1], s=300, c='yellow', 
            marker='*', edgecolors='black', linewidths=2, label='Centroids')

plt.xlabel("Annual Income (k$)", fontsize=12)
plt.ylabel("Spending Score (1-100)", fontsize=12)
plt.title("K-Means Clustering - Mall Customers", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("kmeans_clusters.png")
plt.show()

# ===== Step 8: Cluster Analysis Summary =====
print(f"\n{'='*60}")
print("  CLUSTER ANALYSIS SUMMARY")
print(f"{'='*60}")
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    print(f"\n  Cluster {i} ({len(cluster_data)} customers):")
    print(f"    Avg Income:   ${cluster_data['Annual Income (k$)'].mean():.1f}k")
    print(f"    Avg Spending: {cluster_data['Spending Score (1-100)'].mean():.1f}")
    print(f"    Avg Age:      {cluster_data['Age'].mean():.1f}")