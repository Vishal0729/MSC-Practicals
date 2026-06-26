# Required libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# ===== Step 1: Load the Dataset =====
# Boston Housing dataset (predict house price based on multiple features)
url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
df = pd.read_csv(url)

# --- If file is downloaded locally, use this instead: ---
# df = pd.read_csv("BostonHousing.csv")
# --------------------------------------------------------

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn descriptions:")
print("""
  crim    - Per capita crime rate
  zn      - Proportion of residential land zoned
  indus   - Proportion of non-retail business acres
  chas    - Charles River dummy variable (1=bounds river)
  nox     - Nitric oxide concentration
  rm      - Average number of rooms per dwelling
  age     - Proportion of owner-occupied units built prior to 1940
  dis     - Weighted distances to employment centres
  rad     - Index of accessibility to radial highways
  tax     - Property tax rate per $10,000
  ptratio - Pupil-teacher ratio
  b       - Proportion of Black residents
  lstat   - % lower status of the population
  medv    - Median value of homes in $1000s (TARGET)
""")

# ===== Step 2: Data Exploration =====
print("Dataset Statistics:")
print(df.describe())
print("\nNull values:")
print(df.isnull().sum())
print("\nCorrelation with target (medv):")
print(df.corr()['medv'].sort_values(ascending=False))

# ===== Step 3: Prepare Features (X) and Target (y) =====
X = df.drop(columns=['medv'])   # All columns except target
y = df['medv']                   # Target: median house value

# ===== Step 4: Split into Training (70%) and Testing (30%) =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ===== Step 5: Build Multiple Linear Regression Model =====
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
print("\nMultiple Linear Regression Model trained successfully!")

# Display coefficients
print("\nModel Coefficients:")
for feature, coef in zip(X.columns, lr_model.coef_):
    print(f"  {feature:<10}: {coef:.4f}")
print(f"  {'Intercept':<10}: {lr_model.intercept_:.4f}")

# ===== Step 6: Make Predictions =====
y_pred = lr_model.predict(X_test)

# ===== Step 7: Evaluate Model Accuracy =====
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print(f"\n{'='*50}")
print(f"  MODEL EVALUATION METRICS")
print(f"{'='*50}")
print(f"  R² Score:                {r2:.4f} ({r2*100:.2f}%)")
print(f"  RMSE (Root Mean Sq Err): {rmse:.4f}")
print(f"  MAE (Mean Abs Error):    {mae:.4f}")
print(f"{'='*50}")

# ===== Step 8: Plot Actual vs Predicted =====
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='blue', edgecolors='k')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Multiple Regression - Actual vs Predicted (Boston Housing)")
plt.tight_layout()
plt.savefig("regression_actual_vs_predicted.png")
plt.show()

# ===== Step 9: Plot Residuals =====
residuals = y_test - y_pred
plt.figure(figsize=(8, 5))
plt.scatter(y_pred, residuals, alpha=0.6, color='green', edgecolors='k')
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.tight_layout()
plt.savefig("regression_residuals.png")
plt.show()

# ===== Step 10: Predict for New Data =====
new_data = pd.DataFrame({
    'crim': [0.03], 'zn': [18.0], 'indus': [2.31], 'chas': [0],
    'nox': [0.538], 'rm': [6.5], 'age': [65.0], 'dis': [4.09],
    'rad': [1], 'tax': [296], 'ptratio': [15.3], 'b': [396.9], 'lstat': [4.98]
})
prediction = lr_model.predict(new_data)
print(f"\nPrediction for new house: ${prediction[0]*1000:,.2f}")