from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = load_breast_cancer()
X = data.data
y = data.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Weak Classifier
weak_model = DecisionTreeClassifier(max_depth=1)

weak_model.fit(X_train, y_train)

weak_pred = weak_model.predict(X_test)

weak_accuracy = accuracy_score(y_test, weak_pred)

# AdaBoost Classifier
ada_model = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=50,
    random_state=42
)

ada_model.fit(X_train, y_train)

ada_pred = ada_model.predict(X_test)

ada_accuracy = accuracy_score(y_test, ada_pred)

print("Weak Classifier Accuracy:", weak_accuracy)
print("AdaBoost Accuracy:", ada_accuracy)