# Retrieve Router Location List from IP Data
import pandas as pd
import os

# Input and Output file names
input_file = r'D:/MSC Practicals/Data Science/Practical - 3/Inputs/IP_DATA_CORE.csv'
output_file = r'D:/MSC Practicals/Data Science/Practical - 3/Outputs/pra3-F_Retrieve_Router_Location.csv'

print("Loading:", input_file)

# Read required columns from dataset
data = pd.read_csv(
    input_file,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding="latin-1",
    low_memory=False
)

# Rename "Place Name" to "Place_Name" for consistency
data.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Remove duplicate router locations
router_locations = data.drop_duplicates()

print("Rows:", router_locations.shape[0])
print("Columns:", router_locations.shape[1])

# Save cleaned dataset to Downloads
router_locations.to_csv(output_file, index=False, encoding="latin-1")

print("Saved to:", output_file)
print("Done!")


