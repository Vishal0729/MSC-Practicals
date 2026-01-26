import os
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
import numpy as np

# ---- Setup Base folder ----
Base = "D:/MSC Practicals/Data Science/Practical - 5/Outputs/"
os.makedirs(Base, exist_ok=True)

# ---- 1. Generate BMI Data ----
rows = []
id_counter = 0
for height_cm in range(100, 300, 10):
    for weight_kg in range(30, 300, 5):
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        if bmi <= 18.5:
            category = 1
        elif bmi < 25:
            category = 2
        elif bmi < 30:
            category = 3
        else:
            category = 4
        rows.append({'ID': id_counter, 'Height': height_m, 'Weight': weight_kg, 'BMI': bmi, 'Category': category})
        id_counter += 1

BMI_df = pd.DataFrame(rows)
BMI_df.to_csv(os.path.join(Base, 'BMI.csv'), index=False)

# ---- 2. Save BMI to SQLite ----
for db_name in ['Transform-BMI.db', 'Person-Satellite-BMI.db', 'Dim-BMI.db']:
    db_path = os.path.join(Base, db_name)
    conn = sqlite3.connect(db_path)
    BMI_df.to_sql('BMI', conn, if_exists='replace', index=False)
    conn.close()

# ---- 3. Plot BMI categories ----
markers = {1: '.', 2: 'o', 3: '+', 4: '^'}
plt.figure()
for cat, marker in markers.items():
    sub = BMI_df[BMI_df['Category'] == cat]
    plt.plot(sub['Height'], sub['Weight'], marker, label=f'Category {cat}')
plt.title("BMI Curve")
plt.xlabel("Height (m)")
plt.ylabel("Weight (kg)")
plt.legend()
plt.show()

# ---- 4. Linear Regression: Diabetes ----
diabetes = datasets.load_diabetes()
X = diabetes.data[:, 2:3]  # use 1 feature
y = diabetes.target
X_train, X_test = X[:-30], X[-50:]
y_train, y_test = y[:-30], y[-50:]

reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)

print("Coefficients:", reg.coef_)
print("Mean Squared Error:", np.mean((y_test - y_pred) ** 2))
print("R2 Score:", reg.score(X_test, y_test))

plt.scatter(X_test, y_test, color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=2)
plt.title("Diabetes Prediction")
plt.xlabel("BMI")
plt.ylabel("Disease Progression")
plt.show()
