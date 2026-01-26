# retrieve Billboard Location List – Krennwallner AG
import pandas as pd
import os
# File names (input and output in Downloads)
input_file = r'D:/MSC Practicals/Data Science/Practical - 3/Inputs/DE_Billboard_Locations.csv'
output_file = r'D:/MSC Practicals/Data Science/Practical - 3/Outputs/pra3-G_Retrieve_DE_Billboard_Locations.csv'
print("Loading:", input_file)
# Read required columns
data = pd.read_csv(
    input_file,
    usecols=['Country', 'PlaceName', 'Latitude', 'Longitude'],
    low_memory=False
)
# Rename column for consistency
data.rename(columns={'PlaceName': 'Place_Name'}, inplace=True)
# Remove duplicate billboard locations
billboard_locations = data.drop_duplicates()
print("Rows:", billboard_locations.shape[0])
print("Columns:", billboard_locations.shape[1])
# Create output folder if it somehow doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)
# Save cleaned output in Downloads
billboard_locations.to_csv(output_file, index=False)
print("Saved to:", output_file)
print("Done!")

