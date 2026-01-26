import os
import pandas as pd
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

# Paths
input_file = r"D:/MSC Practicals/Data Science/Practical - 3/Inputs/IP_DATA_ALL.csv"
output_dir = r"D:/MSC Practicals/Data Science/Practical - 3/Outputs"
output_file = os.path.join(output_dir, "Retrieve_Online_Visitor.xml")
os.makedirs(output_dir, exist_ok=True)

# Load CSV and rename columns
df = pd.read_csv(input_file, low_memory=False).rename(columns={
    "Place Name":"Place_Name",
    "First IP Number":"First_IP_Number",
    "Last IP Number":"Last_IP_Number",
    "Post Code":"Post_Code"
})

# Take top 10000 rows
visitordata = df.head(10000)
print(f"Subset Data: Rows={visitordata.shape[0]}, Columns={visitordata.shape[1]}")

# Remove unnamed columns and fix column names for XML
visitordata = visitordata.loc[:, ~visitordata.columns.str.contains('^Unnamed')]
visitordata.columns = [c.replace(" ", "_").replace(":", "_") for c in visitordata.columns]

# Escape values to make XML safe
visitordata = visitordata.applymap(lambda x: escape(str(x)) if pd.notna(x) else "n/a")

# DataFrame → XML
root = ET.Element("root")
for _, row in visitordata.iterrows():
    entry = ET.SubElement(root, "entry")
    for col in visitordata.columns:
        ET.SubElement(entry, col).text = str(row[col])

tree = ET.ElementTree(root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"XML stored at: {output_file}")
print("XML processing completed successfully!")
