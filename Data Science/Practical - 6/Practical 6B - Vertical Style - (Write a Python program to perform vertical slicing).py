import pandas as pd
import sqlite3
import os

base = r"D:/MSC Practicals/Data Science/Practical - 6/"

# Input: Data Warehouse
dw = os.path.join(base, "Inputs/datawarehouse.db")
conn_dw = sqlite3.connect(dw)

# Output: Data Mart
dm = os.path.join(base, "Outputs/6B_datamart.db")
conn_dm = sqlite3.connect(dm)

# Load full table
df = pd.read_sql("SELECT * FROM [Dim-BMI]", conn_dw)

# Vertical slicing → keep only selected columns
vertical = df[["Height", "Weight", "Indicator"]]

# Store in datamart
vertical.to_sql("Dim-BMI-Vertical", conn_dm, if_exists="replace", index=False)

# Print details
print("Full dataset:", df.shape)
print("Vertical sliced dataset:", vertical.shape)

