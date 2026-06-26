# Required libraries
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ===== Step 1: Load the Dataset =====
# Using Iris dataset
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
df = pd.read_csv(url)

# --- If file is downloaded locally, use this instead: ---
# df = pd.read_csv("iris.csv")
# --------------------------------------------------------

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nClass distribution:")
print(df['species'].value_counts())

# ===== Step 2: Prepare Features (X) and Target (y) =====
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
y = df['species']

# ===== Step 3: Split into Training (70%) and Testing (30%) =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ===== Step 4: Feature Scaling (Important for KNN - distance based) =====
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===== Step 5: Build KNN Classifier =====
k = 5  # Number of neighbors
knn_model = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
knn_model.fit(X_train_scaled, y_train)
print(f"\nKNN Model trained successfully! (K={k})")

# ===== Step 6: Make Predictions =====
y_pred = knn_model.predict(X_test_scaled)

# ===== Step 7: Evaluate Model Accuracy =====
accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'='*50}")
print(f"  MODEL ACCURACY: {accuracy * 100:.2f}%")
print(f"{'='*50}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ===== Step 8: Confusion Matrix =====
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Plot Confusion Matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=knn_model.classes_)
disp.plot(cmap='Blues', values_format='d')
plt.title(f"KNN (K={k}) - Confusion Matrix (Iris Dataset)")
plt.tight_layout()
plt.savefig("knn_confusion_matrix.png")
plt.show()

# ===== Step 9: Find Optimal K =====
print("\nFinding optimal K value...")
k_range = range(1, 21)
accuracies = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    pred = knn.predict(X_test_scaled)
    accuracies.append(accuracy_score(y_test, pred))

# Display accuracy for each K
print(f"\n{'K':<5} {'Accuracy':>10}")
print(f"{'-'*5} {'-'*10}")
for k, acc in zip(k_range, accuracies):
    print(f"{k:<5} {acc*100:>9.2f}%")

best_k = list(k_range)[np.argmax(accuracies)]
print(f"\nBest K = {best_k} with Accuracy = {max(accuracies)*100:.2f}%")

# Plot K vs Accuracy
plt.figure(figsize=(8, 5))
plt.plot(k_range, accuracies, 'bo-', linewidth=2, markersize=8)
plt.axvline(x=best_k, color='red', linestyle='--', label=f'Best K={best_k}')
plt.xlabel("K (Number of Neighbors)")
plt.ylabel("Accuracy")
plt.title("KNN - Accuracy vs K Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("knn_k_vs_accuracy.png")
plt.show()

# ===== Step 10: Predict for New Data =====
new_flower = pd.DataFrame({'sepal_length': [5.1], 'sepal_width': [3.5],
                           'petal_length': [1.4], 'petal_width': [0.2]})
new_scaled = scaler.transform(new_flower)
prediction = knn_model.predict(new_scaled)
print(f"\nPrediction for new flower (5.1, 3.5, 1.4, 0.2): {prediction[0]}")