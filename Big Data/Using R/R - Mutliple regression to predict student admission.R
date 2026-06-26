# Required libraries (no extra packages needed - base R handles linear regression)
# library(caret)  # Optional: for advanced metrics

# ===== Step 1: Load the Dataset =====
url <- "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
df <- read.csv(url)

# --- If file is downloaded locally, use this instead: ---
# df <- read.csv("BostonHousing.csv")
# --------------------------------------------------------

cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("\nFirst 5 rows:\n")
print(head(df, 5))

# ===== Step 2: Data Exploration =====
cat("\nDataset Summary:\n")
print(summary(df))
cat("\nNull values:\n")
print(colSums(is.na(df)))
cat("\nCorrelation with target (medv):\n")
correlations <- cor(df)
print(sort(correlations[, "medv"], decreasing = TRUE))

# ===== Step 3: Split into Training (70%) and Testing (30%) =====
set.seed(42)
train_index <- sample(1:nrow(df), 0.7 * nrow(df))
train_data <- df[train_index, ]
test_data <- df[-train_index, ]
cat(sprintf("\nTraining samples: %d\n", nrow(train_data)))
cat(sprintf("Testing samples: %d\n", nrow(test_data)))

# ===== Step 4: Build Multiple Linear Regression Model =====
# medv ~ . means predict medv using ALL other columns
lr_model <- lm(medv ~ ., data = train_data)
cat("\nMultiple Linear Regression Model trained successfully!\n")

# Display model summary (coefficients, R², p-values)
cat("\nModel Summary:\n")
print(summary(lr_model))

# ===== Step 5: Make Predictions =====
y_pred <- predict(lr_model, test_data)
y_test <- test_data$medv

# ===== Step 6: Evaluate Model Accuracy =====
# R² Score
ss_res <- sum((y_test - y_pred)^2)
ss_tot <- sum((y_test - mean(y_test))^2)
r2 <- 1 - (ss_res / ss_tot)

# RMSE
rmse <- sqrt(mean((y_test - y_pred)^2))

# MAE
mae <- mean(abs(y_test - y_pred))

cat(sprintf("\n%s\n", strrep("=", 50)))
cat("  MODEL EVALUATION METRICS\n")
cat(sprintf("%s\n", strrep("=", 50)))
cat(sprintf("  R² Score:                %.4f (%.2f%%)\n", r2, r2 * 100))
cat(sprintf("  RMSE (Root Mean Sq Err): %.4f\n", rmse))
cat(sprintf("  MAE (Mean Abs Error):    %.4f\n", mae))
cat(sprintf("%s\n", strrep("=", 50)))

# ===== Step 7: Plot Actual vs Predicted =====
plot(y_test, y_pred,
     xlab = "Actual Values", ylab = "Predicted Values",
     main = "Multiple Regression - Actual vs Predicted",
     col = "blue", pch = 16)
abline(a = 0, b = 1, col = "red", lwd = 2, lty = 2)

# ===== Step 8: Plot Residuals =====
residuals <- y_test - y_pred
plot(y_pred, residuals,
     xlab = "Predicted Values", ylab = "Residuals",
     main = "Residual Plot",
     col = "green", pch = 16)
abline(h = 0, col = "red", lwd = 2, lty = 2)

# ===== Step 9: Predict for New Data =====
new_data <- data.frame(
  crim = 0.03, zn = 18.0, indus = 2.31, chas = 0,
  nox = 0.538, rm = 6.5, age = 65.0, dis = 4.09,
  rad = 1, tax = 296, ptratio = 15.3, b = 396.9, lstat = 4.98
)
prediction <- predict(lr_model, new_data)
cat(sprintf("\nPrediction for new house: $%s\n", 
            format(prediction * 1000, big.mark = ",", nsmall = 2)))