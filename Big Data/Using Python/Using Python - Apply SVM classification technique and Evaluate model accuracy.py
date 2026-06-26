# Required libraries
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ===== Step 1: Load the Dataset =====
# From URL (GitHub mirror of Kaggle dataset)
url = "https://raw.githubusercontent.com/dataprofessor/data/master/cancer.csv"
df = pd.read_csv(url)

# --- If file is downloaded locally, use this instead: ---
# df = pd.read_csv("data.csv")
# --------------------------------------------------------

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# ===== Step 2: Data Preprocessing =====
# Drop unnecessary columns (id and unnamed)
df = df.drop(columns=['id'], errors='ignore')
df = df.drop(columns=['Unnamed: 32'], errors='ignore')

# Check class distribution
print("\nDiagnosis distribution:")
print(df['diagnosis'].value_counts())
# M = Malignant, B = Benign

# Encode target: M=1, B=0
df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})

# ===== Step 3: Prepare Features (X) and Target (y) =====
X = df.drop(columns=['diagnosis'])
y = df['diagnosis']

# ===== Step 4: Split into Training (70%) and Testing (30%) =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ===== Step 5: Feature Scaling (Important for SVM) =====
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===== Step 6: Build SVM Classifier =====
svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_model.fit(X_train_scaled, y_train)
print("\nSVM Model trained successfully!")
print(f"Kernel: RBF")
print(f"Support Vectors: {svm_model.n_support_}")

# ===== Step 7: Make Predictions =====
y_pred = svm_model.predict(X_test_scaled)

# ===== Step 8: Evaluate Model Accuracy =====
accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'='*50}")
print(f"  MODEL ACCURACY: {accuracy * 100:.2f}%")
print(f"{'='*50}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Benign (0)', 'Malignant (1)']))

# ===== Step 9: Confusion Matrix =====
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Plot
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Benign', 'Malignant'])
disp.plot(cmap='Blues', values_format='d')
plt.title("SVM - Confusion Matrix (Breast Cancer Dataset)")
plt.tight_layout()
plt.savefig("svm_confusion_matrix.png")
plt.show()

# ===== Step 10: Compare Different Kernels =====
print("\n" + "="*50)
print("  KERNEL COMPARISON")
print("="*50)
kernels = ['linear', 'rbf', 'poly']
for k in kernels:
    model = SVC(kernel=k, random_state=42)
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, pred)
    print(f"  Kernel: {k:<10} Accuracy: {acc*100:.2f}%")