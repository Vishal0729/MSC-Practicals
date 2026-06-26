# Required libraries
library(e1071)    # SVM
library(caret)    # Confusion matrix & accuracy

# ===== Step 1: Load the Dataset =====
# From URL
url <- "https://raw.githubusercontent.com/dataprofessor/data/master/cancer.csv"
df <- read.csv(url)

# --- If file is downloaded locally, use this instead: ---
# df <- read.csv("data.csv")
# --------------------------------------------------------

cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("\nFirst 5 rows:\n")
print(head(df, 5))

# ===== Step 2: Data Preprocessing =====
# Drop unnecessary columns
df$id <- NULL
df$X <- NULL  # Unnamed column

# Check class distribution
cat("\nDiagnosis distribution:\n")
print(table(df$diagnosis))

# Convert target to factor
df$diagnosis <- as.factor(df$diagnosis)

# ===== Step 3: Prepare Features (X) and Target (y) =====
X <- df[, -1]   # All columns except diagnosis
y <- df$diagnosis

# ===== Step 4: Split into Training (70%) and Testing (30%) =====
set.seed(42)
train_index <- sample(1:nrow(df), 0.7 * nrow(df))
train_data <- df[train_index, ]
test_data <- df[-train_index, ]
cat(sprintf("\nTraining samples: %d\n", nrow(train_data)))
cat(sprintf("Testing samples: %d\n", nrow(test_data)))

# ===== Step 5: Feature Scaling =====
# Scale all numeric features
train_features <- scale(train_data[, -1])
test_features <- scale(test_data[, -1], 
                       center = attr(train_features, "scaled:center"),
                       scale = attr(train_features, "scaled:scale"))

train_scaled <- data.frame(diagnosis = train_data$diagnosis, train_features)
test_scaled <- data.frame(diagnosis = test_data$diagnosis, test_features)

# ===== Step 6: Build SVM Classifier =====
svm_model <- svm(diagnosis ~ ., data = train_scaled, 
                 kernel = "radial", cost = 1, gamma = 0.01)
cat("\nSVM Model trained successfully!\n")
print(summary(svm_model))

# ===== Step 7: Make Predictions =====
y_pred <- predict(svm_model, test_scaled[, -1])

# ===== Step 8: Evaluate Model Accuracy =====
cm <- confusionMatrix(y_pred, test_scaled$diagnosis)
cat(sprintf("\n%s\n", strrep("=", 50)))
cat(sprintf("  MODEL ACCURACY: %.2f%%\n", cm$overall['Accuracy'] * 100))
cat(sprintf("%s\n", strrep("=", 50)))
cat("\nFull Evaluation:\n")
print(cm)

# ===== Step 9: Confusion Matrix Plot =====
cm_table <- table(Predicted = y_pred, Actual = test_scaled$diagnosis)
cat("\nConfusion Matrix:\n")
print(cm_table)

# Plot
fourfoldplot(cm_table, color = c("red", "green"),
             main = "SVM - Confusion Matrix (Breast Cancer)")

# ===== Step 10: Compare Different Kernels =====
cat(sprintf("\n%s\n", strrep("=", 50)))
cat("  KERNEL COMPARISON\n")
cat(sprintf("%s\n", strrep("=", 50)))

kernels <- c("linear", "radial", "polynomial")
for (k in kernels) {
  model <- svm(diagnosis ~ ., data = train_scaled, kernel = k)
  pred <- predict(model, test_scaled[, -1])
  acc <- sum(pred == test_scaled$diagnosis) / nrow(test_scaled) * 100
  cat(sprintf("  Kernel: %-12s Accuracy: %.2f%%\n", k, acc))
}