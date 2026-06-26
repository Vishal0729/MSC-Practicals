# Required libraries
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ===== Step 1: Load the Iris Dataset =====
url = "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"
df = pd.read_csv(url)
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

# ===== Step 4: Build Decision Tree Classifier =====
dt_classifier = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=42)
dt_classifier.fit(X_train, y_train)
print("\nDecision Tree trained successfully!")

# ===== Step 5: Make Predictions =====
y_pred = dt_classifier.predict(X_test)

# ===== Step 6: Evaluate Model Accuracy =====
accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'='*50}")
print(f"  MODEL ACCURACY: {accuracy * 100:.2f}%")
print(f"{'='*50}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ===== Step 7: Plot Confusion Matrix =====
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Plot
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=dt_classifier.classes_)
disp.plot(cmap='Blues', values_format='d')
plt.title("Decision Tree - Confusion Matrix (Iris Dataset)")
plt.tight_layout()
plt.savefig("confusion_matrix_python.png")
plt.show()

# ===== Step 8 (Bonus): Visualize the Decision Tree =====
plt.figure(figsize=(15, 8))
plot_tree(dt_classifier, feature_names=X.columns.tolist(),
          class_names=dt_classifier.classes_.tolist(),
          filled=True, rounded=True, fontsize=10)
plt.title("Decision Tree Visualization")
plt.tight_layout()
plt.savefig("decision_tree_python.png")
plt.show()