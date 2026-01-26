import pandas as pd

# Read dataset directly from Downloads folder
sFileName = r'D:/MSC Practicals/Data Science/Practical - 2/Input/IP_DATA_CORE.csv'

print("Loading:", sFileName)
IP_DATA_ALL = pd.read_csv(
    sFileName,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding="latin-1"
)

# Rename column for convenience
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Filter London records
LondonData = IP_DATA_ALL[IP_DATA_ALL['Place_Name'] == 'London']

# Select required columns
AllData = LondonData[['Country', 'Place_Name', 'Latitude']]
print("\nAll London Data:\n", AllData)

# Calculate mean & standard deviation of latitude
MeanData = AllData['Latitude'].mean()
StdData = AllData['Latitude'].std()

# Determine bounds
UpperBound = MeanData + StdData
LowerBound = MeanData - StdData
print("\nUpper Bound:", UpperBound)
print("Lower Bound:", LowerBound)

# Outlier detection
OutliersHigher = AllData[AllData['Latitude'] > UpperBound]
OutliersLower = AllData[AllData['Latitude'] < LowerBound]
OutliersNot = AllData[(AllData['Latitude'] >= LowerBound) & (AllData['Latitude'] <= UpperBound)]

print("\nOutliers Higher:\n", OutliersHigher)
print("\nOutliers Lower:\n", OutliersLower)
print("\nNot Outliers:\n", OutliersNot)

