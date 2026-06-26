# Required libraries
library(ggplot2)    # Plotting

# ===== Step 1: Load the Dataset =====
url <- "https://raw.githubusercontent.com/dsrscientist/dataset1/master/Mall_Customers.csv"
df <- read.csv(url)

# --- If file is downloaded locally, use this instead: ---
# df <- read.csv("Mall_Customers.csv")
# --------------------------------------------------------

cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("\nFirst 5 rows:\n")
print(head(df, 5))
cat("\nSummary:\n")
print(summary(df))

# ===== Step 2: Select Features for Clustering =====
X <- df[, c("Annual.Income..k..", "Spending.Score..1.100.")]
colnames(X) <- c("Income", "Spending")
cat("\nFeatures selected: Annual Income & Spending Score\n")

# ===== Step 3: Feature Scaling =====
X_scaled <- scale(X)

# ===== Step 4: Find Optimal K using Elbow Method =====
wcss <- numeric(10)
for (k in 1:10) {
  km <- kmeans(X_scaled, centers = k, nstart = 10)
  wcss[k] <- km$tot.withinss
}

# Plot Elbow Curve
plot(1:10, wcss, type = "b", pch = 16, col = "blue",
     xlab = "Number of Clusters (K)", ylab = "WCSS",
     main = "Elbow Method - Optimal K")
grid()

cat("\nWCSS values:\n")
for (k in 1:10) {
  cat(sprintf("  K=%-3d WCSS=%.2f\n", k, wcss[k]))
}
cat("\nOptimal K = 5 (from elbow point)\n")

# ===== Step 5: Apply K-Means with Optimal K =====
optimal_k <- 5
set.seed(42)
km_model <- kmeans(X_scaled, centers = optimal_k, nstart = 25)

# Add cluster labels to dataframe
df$Cluster <- as.factor(km_model$cluster)
cat(sprintf("\nK-Means applied with K=%d\n", optimal_k))
cat("\nCluster distribution:\n")
print(table(df$Cluster))

# ===== Step 6: Cluster Centers =====
# Inverse transform to original scale
centers_scaled <- km_model$centers
centers_original <- data.frame(
  Income = centers_scaled[, 1] * attr(X_scaled, "scaled:scale")[1] + attr(X_scaled, "scaled:center")[1],
  Spending = centers_scaled[, 2] * attr(X_scaled, "scaled:scale")[2] + attr(X_scaled, "scaled:center")[2]
)
cat("\nCluster Centers (Original Scale):\n")
print(round(centers_original, 2))

# ===== Step 7: Plot Clusters =====
# Using ggplot2
ggplot(df, aes(x = Annual.Income..k.., y = Spending.Score..1.100., color = Cluster)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_point(data = centers_original, aes(x = Income, y = Spending),
             color = "black", size = 8, shape = 8, stroke = 2) +
  labs(x = "Annual Income (k$)", y = "Spending Score (1-100)",
       title = "K-Means Clustering - Mall Customers",
       color = "Cluster") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14))

# Alternative: Base R plot
plot(df$Annual.Income..k.., df$Spending.Score..1.100.,
     col = as.numeric(df$Cluster) + 1, pch = 16, cex = 1.5,
     xlab = "Annual Income (k$)", ylab = "Spending Score (1-100)",
     main = "K-Means Clustering - Mall Customers")
points(centers_original$Income, centers_original$Spending,
       pch = 8, cex = 3, lwd = 3, col = "black")
legend("topright", legend = paste("Cluster", 1:optimal_k),
       col = 2:(optimal_k + 1), pch = 16)

# ===== Step 8: Cluster Analysis Summary =====
cat(sprintf("\n%s\n", strrep("=", 60)))
cat("  CLUSTER ANALYSIS SUMMARY\n")
cat(sprintf("%s\n", strrep("=", 60)))

for (i in 1:optimal_k) {
  cluster_data <- df[df$Cluster == i, ]
  cat(sprintf("\n  Cluster %d (%d customers):\n", i, nrow(cluster_data)))
  cat(sprintf("    Avg Income:   $%.1fk\n", mean(cluster_data$Annual.Income..k..)))
  cat(sprintf("    Avg Spending: %.1f\n", mean(cluster_data$Spending.Score..1.100.)))
  cat(sprintf("    Avg Age:      %.1f\n", mean(cluster_data$Age)))
}