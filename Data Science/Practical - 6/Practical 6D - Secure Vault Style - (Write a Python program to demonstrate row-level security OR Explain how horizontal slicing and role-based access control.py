import os
import pandas as pd
import sqlite3 as sq

# Database locations in base
base = r"D:/MSC Practicals/Data Science/Practical - 6/"
dw_db = os.path.join(base, "Inputs/datawarehouse.db")
dm_db = os.path.join(base, "Inputs/datamart.db")

# Connect
dw = sq.connect(dw_db)
dm = sq.connect(dm_db)

# Full table (for info only)
df = pd.read_sql("SELECT * FROM [Dim-BMI];", dw)

# Secure filtered table
secure_df = pd.read_sql("""
    SELECT Height, Weight, Indicator,
           CASE Indicator
                WHEN 1 THEN 'Pip'
                WHEN 2 THEN 'Norman'
                WHEN 3 THEN 'Grant'
                ELSE 'Sam'
           END AS Name
    FROM [Dim-BMI]
    WHERE Indicator > 2
    ORDER BY Height, Weight;
""", dw)

# Save secure table
secure_df.to_sql("Dim-BMI-Secure", dm, if_exists="replace", index=False)

# Load only Sam's rows (restricted view)
sam_df = pd.read_sql("SELECT * FROM [Dim-BMI-Secure] WHERE Name='Sam';", dm)

print(sam_df)

