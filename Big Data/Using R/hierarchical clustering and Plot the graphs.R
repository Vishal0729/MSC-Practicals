# Required libraries
library(ggplot2)      # Plotting
library(factoextra)   # Dendrogram & cluster visualization
library(cluster)      # Silhouette score

# ===== Step 1: Load the Dataset =====
url <- "https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data"
columns <- c("Class", "Alcohol", "Malic_Acid", "Ash", "Alcalinity_of_Ash",
             "Magnesium", "Total_Phenols", "Flavanoids", "Nonflavanoid_Phenols",
             "Proanthocyanins", "Color_Intensity", "Hue", "OD280_OD315", "Proline")
df <- read.csv(url, header = FALSE, col.names = columns)

# --- If file is downloaded locally, use this instead: ---
# df <- read.csv("wine.data", header = FALSE, col.names = columns)
# --------------------------------------------------------

cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("\nFirst 5 rows:\n")
print(head(df, 5))
cat("\nClass distribution:\n")
print(table(df$Class))

# ===== Step 2: Prepare Features =====
actual_labels <- df$Class
X <- df[, -1]  # Remove Class column

# ===== Step 3: Feature Scaling =====
X_scaled <- scale(X)
cat("\nFeatures scaled using scale()\n")

# ===== Step 4: Compute Distance Matrix =====
dist_matrix <- dist(X_scaled, method = "euclidean")

# ===== Step 5: Perform Hierarchical Clustering =====
hc_ward <- hclust(dist_matrix, method = "ward.D2")
hc_complete <- hclust(dist_matrix, method = "complete")
hc_average <- hclust(dist_matrix, method = "average")
cat("\nHierarchical clustering computed (Ward, Complete, Average)\n")

# ===== Step 6: Plot Dendrogram (Ward's Method) =====
plot(hc_ward, cex = 0.5, hang = -1,
     main = "Dendrogram - Ward's Method (Wine Dataset)",
     xlab = "Samples", ylab = "Distance")
rect.hclust(hc_ward, k = 3, border = c("red", "blue", "green"))

# ===== Step 7: Plot Dendrograms for All Methods =====
par(mfrow = c(1, 3))

# Ward
plot(hc_ward, cex = 0.4, hang = -1, main = "Ward's Method")
rect.hclust(hc_ward, k = 3, border = "red")

# Complete
plot(hc_complete, cex = 0.4, hang = -1, main = "Complete Linkage")
rect.hclust(hc_complete, k = 3, border = "red")

# Average
plot(hc_average, cex = 0.4, hang = -1, main = "Average Linkage")
rect.hclust(hc_average, k = 3, border = "red")

par(mfrow = c(1, 1))  # Reset layout

# ===== Step 8: Cut Dendrogram to Form Clusters =====
n_clusters <- 3
clusters <- cutree(hc_ward, k = n_clusters)
df$Cluster <- as.factor(clusters)

cat(sprintf("\nClusters formed (K=%d):\n", n_clusters))
cat("\nCluster distribution:\n")
print(table(clusters))

# ===== Step 9: Evaluate Clustering =====
sil <- silhouette(clusters, dist_matrix)
sil_avg <- mean(sil[, 3])
cat(sprintf("\nSilhouette Score: %.4f\n", sil_avg))

# Plot Silhouette
plot(sil, col = 1:n_clusters, border = NA,
     main = "Silhouette Plot - Hierarchical Clustering")

# ===== Step 10: Plot Clusters (2D - First 2 Features) =====
plot(X_scaled[, 1], X_scaled[, 2],
     col = as.numeric(df$Cluster) + 1, pch = 16, cex = 1.5,
     xlab = "Alcohol (Scaled)", ylab = "Malic Acid (Scaled)",
     main = "Hierarchical Clustering - Wine Dataset (Ward's)")
legend("topright", legend = paste("Cluster", 1:n_clusters),
       col = 2:(n_clusters + 1), pch = 16)

# ===== Step 11: Plot Clusters using PCA =====
pca <- prcomp(X_scaled)
pca_data <- data.frame(PC1 = pca$x[, 1], PC2 = pca$x[, 2], Cluster = df$Cluster)

# Variance explained
var_explained <- summary(pca)$importance[2, 1:2] * 100

# ggplot2 version
ggplot(pca_data, aes(x = PC1, y = PC2, color = Cluster)) +
  geom_point(size = 3, alpha = 0.7) +
  labs(x = paste0("PC1 (", round(var_explained[1], 1), "% variance)"),
       y = paste0("PC2 (", round(var_explained[2], 1), "% variance)"),
       title = "Hierarchical Clustering - PCA Projection (Wine Dataset)") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14))

# Alternative: using factoextra (best visualization)
fviz_cluster(list(data = X_scaled, cluster = clusters),
             geom = "point", pointsize = 2,
             main = "Hierarchical Clustering - Wine Dataset")

# ===== Step 12: Cluster Summary =====
cat(sprintf("\n%s\n", strrep("=", 60)))
cat("  CLUSTER SUMMARY\n")
cat(sprintf("%s\n", strrep("=", 60)))

for (i in 1:n_clusters) {
  cluster_data <- df[df$Cluster == i, ]
  cat(sprintf("\n  Cluster %d (%d samples):\n", i, nrow(cluster_data)))
  cat(sprintf("    Avg Alcohol:         %.2f\n", mean(cluster_data$Alcohol)))
  cat(sprintf("    Avg Flavanoids:      %.2f\n", mean(cluster_data$Flavanoids)))
  cat(sprintf("    Avg Color Intensity: %.2f\n", mean(cluster_data$Color_Intensity)))
  cat(sprintf("    Avg Proline:         %.2f\n", mean(cluster_data$Proline)))
}