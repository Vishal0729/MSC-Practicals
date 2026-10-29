# Practical No. 5: Support Vector Machine (SVM)

# Step 1: Import Libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Step 2: Load Dataset
iris = load_iris()

# Use only first two classes (Binary Classification)
X = iris.data[:100]
y = iris.target[:100]

# Step 3: Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Step 4: Train SVM Model
model = SVC(kernel='linear', C=1.0)
model.fit(X_train, y_train)

# Step 5: Predict Test Data
y_pred = model.predict(X_test)

# Step 6: Evaluate Model
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))