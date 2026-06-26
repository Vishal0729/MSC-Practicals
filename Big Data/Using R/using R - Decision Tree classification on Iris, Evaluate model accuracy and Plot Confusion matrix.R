# Required libraries
library(rpart)        # Decision Tree
library(rpart.plot)   # Tree visualization
library(caret)        # Confusion matrix & accuracy

# ===== Step 1: Load the Iris Dataset =====
url <- "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"
df <- read.csv(url)
cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("\nFirst 5 rows:\n")
print(head(df, 5))
cat("\nClass distribution:\n")
print(table(df$species))

# ===== Step 2: Convert target to factor =====
df$species <- as.factor(df$species)

# ===== Step 3: Split into Training (70%) and Testing (30%) =====
set.seed(42)
train_index <- sample(1:nrow(df), 0.7 * nrow(df))
train_data <- df[train_index, ]
test_data <- df[-train_index, ]
cat(sprintf("\nTraining samples: %d\n", nrow(train_data)))
cat(sprintf("Testing samples: %d\n", nrow(test_data)))

# ===== Step 4: Build Decision Tree Classifier =====
dt_model <- rpart(species ~ sepal_length + sepal_width + petal_length + petal_width,
                  data = train_data, method = "class")
cat("\nDecision Tree trained successfully!\n")

# ===== Step 5: Make Predictions =====
y_pred <- predict(dt_model, test_data, type = "class")

# ===== Step 6: Evaluate Model Accuracy =====
cm <- confusionMatrix(y_pred, test_data$species)
cat(sprintf("\n%s\n", strrep("=", 50)))
cat(sprintf("  MODEL ACCURACY: %.2f%%\n", cm$overall['Accuracy'] * 100))
cat(sprintf("%s\n", strrep("=", 50)))
cat("\nFull Evaluation:\n")
print(cm)

# ===== Step 7: Plot Confusion Matrix =====
# Method: Using base R heatmap
cm_table <- as.matrix(table(Predicted = y_pred, Actual = test_data$species))
cat("\nConfusion Matrix:\n")
print(cm_table)

# Plot confusion matrix as heatmap
heatmap(cm_table, Rowv = NA, Colv = NA, col = heat.colors(256),
        scale = "none", margins = c(8, 8),
        main = "Decision Tree - Confusion Matrix (Iris Dataset)")

# ===== Step 8 (Bonus): Visualize the Decision Tree =====
rpart.plot(dt_model, main = "Decision Tree - Iris Dataset",
           extra = 104, under = TRUE, faclen = 0)