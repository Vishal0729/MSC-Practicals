# Required libraries
library(class)    # KNN
library(caret)    # Confusion matrix & accuracy

# ===== Step 1: Load the Dataset =====
url <- "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
df <- read.csv(url)

# --- If file is downloaded locally, use this instead: ---
# df <- read.csv("iris.csv")
# --------------------------------------------------------

cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("\nFirst 5 rows:\n")
print(head(df, 5))
cat("\nClass distribution:\n")
print(table(df$species))

# ===== Step 2: Prepare Features and Target =====
X <- df[, 1:4]  # sepal_length, sepal_width, petal_length, petal_width
y <- as.factor(df$species)

# ===== Step 3: Split into Training (70%) and Testing (30%) =====
set.seed(42)
train_index <- sample(1:nrow(df), 0.7 * nrow(df))
X_train <- X[train_index, ]
X_test <- X[-train_index, ]
y_train <- y[train_index]
y_test <- y[-train_index]
cat(sprintf("\nTraining samples: %d\n", length(y_train)))
cat(sprintf("Testing samples: %d\n", length(y_test)))

# ===== Step 4: Feature Scaling =====
X_train_scaled <- scale(X_train)
X_test_scaled <- scale(X_test,
                       center = attr(X_train_scaled, "scaled:center"),
                       scale = attr(X_train_scaled, "scaled:scale"))

# ===== Step 5: Build KNN Classifier =====
k <- 5
y_pred <- knn(train = X_train_scaled, test = X_test_scaled, cl = y_train, k = k)
cat(sprintf("\nKNN Model trained and predicted! (K=%d)\n", k))

# ===== Step 6: Evaluate Model Accuracy =====
cm <- confusionMatrix(y_pred, y_test)
cat(sprintf("\n%s\n", strrep("=", 50)))
cat(sprintf("  MODEL ACCURACY: %.2f%%\n", cm$overall['Accuracy'] * 100))
cat(sprintf("%s\n", strrep("=", 50)))
cat("\nFull Evaluation:\n")
print(cm)

# ===== Step 7: Confusion Matrix =====
cm_table <- table(Predicted = y_pred, Actual = y_test)
cat("\nConfusion Matrix:\n")
print(cm_table)

# Plot Confusion Matrix
fourfoldplot(cm_table, color = c("red", "green"),
             main = sprintf("KNN (K=%d) - Confusion Matrix (Iris)", k))

# ===== Step 8: Find Optimal K =====
cat("\nFinding optimal K value...\n")
k_range <- 1:20
accuracies <- numeric(length(k_range))

for (i in seq_along(k_range)) {
  pred <- knn(train = X_train_scaled, test = X_test_scaled, cl = y_train, k = k_range[i])
  accuracies[i] <- sum(pred == y_test) / length(y_test)
}

# Display accuracy for each K
cat(sprintf("\n%-5s %10s\n", "K", "Accuracy"))
cat(sprintf("%-5s %10s\n", strrep("-", 5), strrep("-", 10)))
for (i in seq_along(k_range)) {
  cat(sprintf("%-5d %9.2f%%\n", k_range[i], accuracies[i] * 100))
}

best_k <- k_range[which.max(accuracies)]
cat(sprintf("\nBest K = %d with Accuracy = %.2f%%\n", best_k, max(accuracies) * 100))

# Plot K vs Accuracy
plot(k_range, accuracies, type = "b", col = "blue", pch = 16,
     xlab = "K (Number of Neighbors)", ylab = "Accuracy",
     main = "KNN - Accuracy vs K Value")
abline(v = best_k, col = "red", lty = 2)
legend("bottomright", legend = paste("Best K =", best_k), col = "red", lty = 2)

# ===== Step 9: Predict for New Data =====
new_flower <- data.frame(sepal_length = 5.1, sepal_width = 3.5,
                         petal_length = 1.4, petal_width = 0.2)
new_scaled <- scale(new_flower,
                    center = attr(X_train_scaled, "scaled:center"),
                    scale = attr(X_train_scaled, "scaled:scale"))
prediction <- knn(train = X_train_scaled, test = new_scaled, cl = y_train, k = best_k)
cat(sprintf("\nPrediction for new flower (5.1, 3.5, 1.4, 0.2): %s\n", prediction))