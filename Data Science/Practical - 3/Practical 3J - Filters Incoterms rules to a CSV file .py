import os
import pandas as pd

# ----------------- CONFIG -----------------
IncoTerm = 'EXW'
Base = r"D:/MSC Practicals/Data Science/Practical - 3/"
InputFilePath = os.path.join(Base, "Inputs/Incoterm_2010.csv")
OutputFilePath = os.path.join(Base, f"Outputs/pra3-J_Retrieve_Incoterm_{IncoTerm}_RuleSet.csv")

# ----------------- LOAD AND FILTER -----------------
print(f"Loading CSV: {InputFilePath}")
df = pd.read_csv(InputFilePath, low_memory=False)

# Filter rows matching the specified Incoterm
df_rule = df[df['Shipping_Term'] == IncoTerm]

# ----------------- SAVE OUTPUT -----------------
df_rule.to_csv(OutputFilePath, index=False)
print(f"Filtered data stored at: {OutputFilePath}")
print(f"Rows: {df_rule.shape[0]}, Columns: {df_rule.shape[1]}")
print("Processing completed successfully!")

