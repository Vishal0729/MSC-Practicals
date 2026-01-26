import os
import pandas as pd

# Paths
base = r"D:/MSC Practicals/Data Science/Practical - 6/"
input_file = os.path.join(base, "Inputs/Assess_Shipping_Routes.txt")

# Load dataset
df = pd.read_csv(input_file, sep='|', encoding='latin-1')

# Filter for HQ-KA13 routes
routes = df[df['StartAt'] == 'WH-KA13']

# Max distance route cost
max_distance = routes['Measure'].max()
daily_cost = round((max_distance * 1.5 * 2), 2)   # £1.5 per mile × 2 trips

# Monthly average miles
avg_distance = routes['Measure'].mean()
monthly_miles = round((avg_distance * 2 * 30), 2)

print("Most expensive route per day (£):", daily_cost)
print("Average miles per month:", monthly_miles)


