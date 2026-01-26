import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Load CSV from Base
Base = r"D:/MSC Practicals/Data Science/Practical - 6/"
input_file = os.path.join(Base, "Inputs/Assess-DE-Billboard-Visitor.csv")
output_png = os.path.join(Base, "Outputs/Organise-Billboards.png")
df = pd.read_csv(input_file, encoding="latin-1")
# Pick 20 random samples for clarity
sample_idx = np.random.choice(df.index, 20, replace=False)
# Create lists of nodes
nodes = set()
for i in sample_idx:
    billboard = f"{df.loc[i,'BillboardPlaceName']} ({df.loc[i,'BillboardCountry']})"
    visitor_place = f"{df.loc[i,'VisitorPlaceName']}"
    visitor_country = f"{df.loc[i,'VisitorCountry']}"
    nodes.add(billboard)
    nodes.add(visitor_place)
    nodes.add(visitor_country)
nodes = list(nodes)
# Position nodes in a circle
angle_step = 2 * np.pi / len(nodes)
positions = {}
for i, node in enumerate(nodes):
    x = 10 * np.cos(i * angle_step)
    y = 10 * np.sin(i * angle_step)
    positions[node] = (x, y)
# Plot
plt.figure(figsize=(12, 12))
# Draw edges
for i in sample_idx:
    billboard = f"{df.loc[i,'BillboardPlaceName']} ({df.loc[i,'BillboardCountry']})"
    visitor_place = f"{df.loc[i,'VisitorPlaceName']}"
    visitor_country = f"{df.loc[i,'VisitorCountry']}"
    # draw: billboard → visitor place
    x_vals = [positions[billboard][0], positions[visitor_place][0]]
    y_vals = [positions[billboard][1], positions[visitor_place][1]]
    plt.plot(x_vals, y_vals, color='red', linestyle='dashed')
    # draw: visitor place → visitor country
    x_vals = [positions[visitor_place][0], positions[visitor_country][0]]
    y_vals = [positions[visitor_place][1], positions[visitor_country][1]]
    plt.plot(x_vals, y_vals, color='blue', linestyle='solid')
# Draw nodes & labels
for node, (x, y) in positions.items():
    plt.scatter(x, y, color="black")
    plt.text(x, y, node, fontsize=8, ha='center', va='center')
plt.title("Billboard - Visitor Network (NO NetworkX)")
plt.axis("off")
# Save in Base
plt.savefig(output_png, dpi=600, bbox_inches='tight')
plt.show()
print("Graph saved at:", output_png)
