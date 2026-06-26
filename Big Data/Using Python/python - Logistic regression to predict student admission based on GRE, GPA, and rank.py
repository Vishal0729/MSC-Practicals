# Required libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ===== Step 1: Load the Dataset =====
url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/admission.csv"
df = pd.read_csv(url)

# --- If file is downloaded locally, use this instead: ---
# df = pd.read_csv("admission.csv")
# --------------------------------------------------------

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn names:", df.columns.tolist())

# ===== Step 2: Data Exploration =====
print("\nDataset Info:")
print(df.describe())
print("\nAdmission distribution (0=No, 1=Yes):")
print(df['admit'].value_counts())
print("\nNull values:")
print(df.isnull().sum())

# ===== Step 3: Prepare Features (X) and Target (y) =====
X = df[['gre', 'gpa', 'rank']]
y = df['admit']

# ===== Step 4: Split into Training (70%) and Testing (30%) =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ===== Step 5: Feature Scaling =====
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===== Step 6: Build Logistic Regression Model =====
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
print("\nLogistic Regression Model trained successfully!")

# Display coefficients
print("\nModel Coefficients:")
for feature, coef in zip(['gre', 'gpa', 'rank'], lr_model.coef_[0]):
    print(f"  {feature:<6}: {coef:.4f}")
print(f"  Intercept: {lr_model.intercept_[0]:.4f}")

# ===== Step 7: Make Predictions =====
y_pred = lr_model.predict(X_test_scaled)
y_prob = lr_model.predict_proba(X_test_scaled)[:, 1]  # Probability of admission

# ===== Step 8: Evaluate Model Accuracy =====
accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'='*50}")
print(f"  MODEL ACCURACY: {accuracy * 100:.2f}%")
print(f"{'='*50}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Not Admitted (0)', 'Admitted (1)']))

# ===== Step 9: Confusion Matrix =====
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Plot
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Not Admitted', 'Admitted'])
disp.plot(cmap='Blues', values_format='d')
plt.title("Logistic Regression - Confusion Matrix (Student Admission)")
plt.tight_layout()
plt.savefig("logistic_regression_cm.png")
plt.show()

# ===== Step 10: Predict for New Student =====
new_student = pd.DataFrame({'gre': [750], 'gpa': [3.8], 'rank': [1]})
new_student_scaled = scaler.transform(new_student)
prediction = lr_model.predict(new_student_scaled)
probability = lr_model.predict_proba(new_student_scaled)[0][1]
print(f"\nPrediction for new student (GRE=750, GPA=3.8, Rank=1):")
print(f"  Admitted: {'Yes' if prediction[0]==1 else 'No'}")
print(f"  Probability of Admission: {probability*100:.2f}%")