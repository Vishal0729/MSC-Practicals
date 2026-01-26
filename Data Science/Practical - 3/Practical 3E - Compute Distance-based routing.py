import pandas as pd
from math import radians, cos, sin, asin, sqrt

# Haversine function → Calculates distance between two geo points
def haversine(lon1, lat1, lon2, lat2, unit):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 if unit == 'km' else 3956
    return round(c * r, 3)

# Load dataset from Downloads
file_path = r"D:/MSC Practicals/Data Science/Practical - 3/Inputs/IP_DATA_CORE.csv"
print("Loading:", file_path)
df = pd.read_csv(file_path, usecols=['Country', 'Place Name', 'Latitude', 'Longitude'], encoding="latin-1")

# Clean and prepare data
df.drop_duplicates(inplace=True)
df.rename(columns={'Place Name': 'Place_Name'}, inplace=True)
df.insert(0, 'Key', 1)

# Make every place pair with every other (cross join)
cross = pd.merge(df, df, on='Key').drop('Key', axis=1)

# Rename columns to from / to format
cross.rename(columns={
    'Country_x': 'Country_from', 'Country_y': 'Country_to',
    'Place_Name_x': 'Place_Name_from', 'Place_Name_y': 'Place_Name_to',
    'Latitude_x': 'Latitude_from',   'Latitude_y': 'Latitude_to',
    'Longitude_x': 'Longitude_from', 'Longitude_y': 'Longitude_to'
}, inplace=True)

# Calculate distance columns
cross['Distance_KM'] = cross.apply(
    lambda row: haversine(row['Longitude_from'], row['Latitude_from'],
                          row['Longitude_to'], row['Latitude_to'], 'km'), axis=1)

cross['Distance_Miles'] = cross.apply(
    lambda row: haversine(row['Longitude_from'], row['Latitude_from'],
                          row['Longitude_to'], row['Latitude_to'], 'miles'), axis=1)

# Save output to Downloads
output_path = r"D:/MSC Practicals/Data Science/Practical - 3/Outputs/pra3-E_Retrieve_IP_Routing.csv"
cross.to_csv(output_path, index=False, encoding="latin-1")
print("Saved to:", output_path)
print("Done!")

