import pandas as pd
import sqlite3 as sq
# Input Agreement (use local path instead of GitHub URL)
sInputFileName = "D:/MSC Practicals/Data Science/Practical - 1/Inputs/utility.db"
sInputTable = 'Country_Code'
# Connect to database and read data
conn = sq.connect(sInputFileName)
sSQL = f'SELECT * FROM {sInputTable};'
InputData = pd.read_sql_query(sSQL, conn)
print('Input Data Values ===================================')
print(InputData)
print('=====================================================')
# Processing Rules
ProcessData = InputData.copy()
# Remove unnecessary columns safely (ignore if missing)
ProcessData.drop(['ISO-2-CODE', 'ISO-3-CODE', 'ISO-3-Code'], axis=1, inplace=True, errors='ignore')
# Rename columns (only if they exist in the table)
rename_map = {}
if 'Country' in ProcessData.columns:
    rename_map['Country'] = 'CountryName'
if 'ISO-M49' in ProcessData.columns:
    rename_map['ISO-M49'] = 'CountryNumber'
ProcessData.rename(columns=rename_map, inplace=True)
# Set new Index if column exists
if 'CountryNumber' in ProcessData.columns:
    ProcessData.set_index('CountryNumber', inplace=True)
# Sort data if column exists
if 'CountryName' in ProcessData.columns:
    ProcessData.sort_values('CountryName', ascending=False, inplace=True)
print('Processed Data Values =================================')
print(ProcessData)
print('=====================================================')
# Output Agreement
OutputData = ProcessData.reset_index()  # Reset index to include CountryNumber in CSV
sOutputFileName = "D:/MSC Practicals/Data Science/Practical - 1/Outputs/1D_HORUS-CSV-Country.csv"
OutputData.to_csv(sOutputFileName, index=False)
print('Database to HORUS - Done')

