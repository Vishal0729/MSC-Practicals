# Required libraries
library(caret)    # Confusion matrix & accuracy
library(pROC)    # ROC curve (optional)

# ===== Step 1: Load the Dataset =====
url <- "https://raw.githubusercontent.com/dsrscientist/dataset1/master/admission.csv"
df <- read.csv(url)

# --- If file is downloaded locally, use this instead: ---
# df <- read.csv("admission.csv")
# --------------------------------------------------------

cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("\nFirst 5 rows:\n")
print(head(df, 5))

# ===== Step 2: Data Exploration =====
cat("\nDataset Summary:\n")
print(summary(df))
cat("\nAdmission distribution (0=No, 1=Yes):\n")
print(table(df$admit))
cat("\nNull values:\n")
print(colSums(is.na(df)))

# ===== Step 3: Prepare Data =====
# Convert admit to factor for classification
df$admit <- as.factor(df$admit)

# ===== Step 4: Split into Training (70%) and Testing (30%) =====
set.seed(42)
train_index <- sample(1:nrow(df), 0.7 * nrow(df))
train_data <- df[train_index, ]
test_data <- df[-train_index, ]
cat(sprintf("\nTraining samples: %d\n", nrow(train_data)))
cat(sprintf("Testing samples: %d\n", nrow(test_data)))

# ===== Step 5: Build Logistic Regression Model =====
# glm with family=binomial performs logistic regression
lr_model <- glm(admit ~ gre + gpa + rank, data = train_data, family = binomial)
cat("\nLogistic Regression Model trained successfully!\n")

# Display model summary (coefficients, significance)
cat("\nModel Summary:\n")
print(summary(lr_model))

# ===== Step 6: Make Predictions =====
# Get probabilities
y_prob <- predict(lr_model, test_data, type = "response")

# Convert probabilities to class labels (threshold = 0.5)
y_pred <- ifelse(y_prob > 0.5, 1, 0)
y_pred <- as.factor(y_pred)

# ===== Step 7: Evaluate Model Accuracy =====
cm <- confusionMatrix(y_pred, test_data$admit)
cat(sprintf("\n%s\n", strrep("=", 50)))
cat(sprintf("  MODEL ACCURACY: %.2f%%\n", cm$overall['Accuracy'] * 100))
cat(sprintf("%s\n", strrep("=", 50)))
cat("\nFull Evaluation:\n")
print(cm)

# ===== Step 8: Confusion Matrix =====
cm_table <- table(Predicted = y_pred, Actual = test_data$admit)
cat("\nConfusion Matrix:\n")
print(cm_table)

# Plot
fourfoldplot(cm_table, color = c("red", "green"),
             main = "Logistic Regression - Confusion Matrix (Admission)")

# ===== Step 9: Predict for New Student =====
new_student <- data.frame(gre = 750, gpa = 3.8, rank = 1)
prob <- predict(lr_model, new_student, type = "response")
cat(sprintf("\nPrediction for new student (GRE=750, GPA=3.8, Rank=1):\n"))
cat(sprintf("  Admitted: %s\n", ifelse(prob > 0.5, "Yes", "No")))
cat(sprintf("  Probability of Admission: %.2f%%\n", prob * 100))