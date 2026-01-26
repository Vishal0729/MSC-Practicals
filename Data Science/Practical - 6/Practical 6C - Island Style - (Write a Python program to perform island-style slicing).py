import pandas as pd
import sqlite3
import os

base = r"D:/MSC Practicals/Data Science/Practical - 6/"

# Input: Data Warehouse
dw = os.path.join(base, "Inputs/datawarehouse.db")
conn_dw = sqlite3.connect(dw)

# Output: Data Mart
dm = os.path.join(base, "Outputs/6C_datamart.db")
conn_dm = sqlite3.connect(dm)

# Load full table
df = pd.read_sql("SELECT * FROM [Dim-BMI]", conn_dw)

# Island-style slicing = rows + columns
island = df[df["Indicator"] > 2][["Height", "Weight", "Indicator"]]

# Save into datamart
island.to_sql("Dim-BMI-Island", conn_dm, if_exists="replace", index=False)

# Print summary
print("Full dataset:", df.shape)
print("Island sliced dataset:", island.shape)

