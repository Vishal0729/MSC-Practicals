import os
import pandas as pd
# Base folder
Base = 'D:/MSC Practicals/Data Science/Practical - 3'
# Correct input file path
file_input = f'{Base}/Inputs/IP_DATA_ALL.csv'
print("Loading:", file_input)
data = pd.read_csv(file_input, encoding="latin-1", low_memory=False)
# Create output folder
output_dir = f'{Base}/Outputs/Cleaned_IP_Data'
os.makedirs(output_dir, exist_ok=True)
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])
# Clean column names
data.columns = [col.strip().replace(" ", ".") for col in data.columns]
# Add row index label
data.index.name = "RowID"
# Save cleaned file
output_file = f'{output_dir}/pra3-B_Retrieve_IP_DATA.csv'
data.to_csv(output_file, index=True, encoding="latin-1")
print("Output File Saved At:", output_file)
print("Done!")

