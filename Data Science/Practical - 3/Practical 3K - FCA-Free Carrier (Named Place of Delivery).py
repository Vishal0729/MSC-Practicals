# -*- coding: utf-8 -*-
import os
import pandas as pd

# ----------------- CONFIG -----------------
IncoTerm = 'FCA'
Base = r"D:/MSC Practicals/Data Science/Practical - 3/"  # Use Base folder for both input and output
InputFile = os.path.join(Base, "Inputs/Incoterm_2010.csv")
OutputFile = os.path.join(Base, f"Outputs/Retrieve_Incoterm_{IncoTerm}_RuleSet.csv")

# ----------------- LOAD AND FILTER -----------------
print(f"Loading CSV: {InputFile}")
df = pd.read_csv(InputFile, low_memory=False)

# Filter rows matching the specified Incoterm
df_rule = df[df['Shipping_Term'] == IncoTerm]

# ----------------- SAVE OUTPUT -----------------
df_rule.to_csv(OutputFile, index=False)
print(f"Filtered data stored at: {OutputFile}")
print(f"Rows: {df_rule.shape[0]}, Columns: {df_rule.shape[1]}")
print("Processing completed successfully!")
