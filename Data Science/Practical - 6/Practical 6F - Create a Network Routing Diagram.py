import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Paths
Base = r"D:/MSC Practicals/Data Science/Practical - 6/"
input_file = os.path.join(Base, "Inputs/Assess-Network-Routing-Company.csv")
output_file = os.path.join(Base, "Outputs/Organise-Network-Routing-Company.png")
# Load data
df = pd.read_csv(input_file, encoding="latin-1")
# Unique countries and mapping
countries = df['Company_Country_Name'].unique()
country_idx = {country: i for i, country in enumerate(countries)}
# Positions
angle_step = 2 * np.pi / len(countries)
radius = 5
positions = {}
# Place countries in a circle
for i, country in enumerate(countries):
    x = radius * np.cos(i * angle_step)
    y = radius * np.sin(i * angle_step)
    positions[country] = (x, y)
# Place company nodes near their country
for _, row in df.iterrows():
    country = row['Company_Country_Name']
    place = f"{row['Company_Place_Name']} ({country})"
    cx, cy = positions[country]
    offset = np.random.rand(2) * 1.0 - 0.5
    positions[place] = (cx + offset[0], cy + offset[1])
# Plot edges
plt.figure(figsize=(10,10))
# Connect countries to their companies
for _, row in df.iterrows():
    country = row['Company_Country_Name']
    place = f"{row['Company_Place_Name']} ({country})"
    x_vals = [positions[country][0], positions[place][0]]
    y_vals = [positions[country][1], positions[place][1]]
    plt.plot(x_vals, y_vals, color='red', linestyle='dashed')
# Connect countries to each other
for i in range(len(countries)):
    for j in range(i+1, len(countries)):
        x_vals = [positions[countries[i]][0], positions[countries[j]][0]]
        y_vals = [positions[countries[i]][1], positions[countries[j]][1]]
        plt.plot(x_vals, y_vals, color='red', linestyle='dashed')
# Draw nodes
for node, (x, y) in positions.items():
    if node in countries:
        plt.scatter(x, y, color='black', s=100)
        plt.text(x, y, node, fontsize=10, ha='center', va='center', color='blue')
    else:
        plt.scatter(x, y, color='black', s=50)
        plt.text(x, y, node, fontsize=8, ha='center', va='center')
plt.axis('off')
plt.title("Countries and Company Places (Network-like Layout)")
# SAVE PNG IN Base
plt.savefig(output_file, dpi=600, bbox_inches='tight')
plt.show()
print("Saved PNG at:", output_file)