import pandas as pd
import sqlite3
import os

# Folder path
base = r"D:/MSC Practicals/Data Science/Practical - 6/"

# Input Data Warehouse DB
dw = os.path.join(base, "Inputs/datawarehouse.db")
conn_dw = sqlite3.connect(dw)

# Output Data Mart DB
dm = os.path.join(base, "Outputs/6A_datamart.db")
conn_dm = sqlite3.connect(dm)

# Load full table
df = pd.read_sql("SELECT * FROM [Dim-BMI]", conn_dw)

# Horizontal slicing
filtered = df[(df["Height"] > 1.5) & (df["Indicator"] == 1)]

# Store filtered rows in datamart
filtered.to_sql("Dim-BMI", conn_dm, if_exists="replace", index=False)

# Print counts
print("Full rows:", df.shape[0])
print("Filtered rows:", filtered.shape[0])


