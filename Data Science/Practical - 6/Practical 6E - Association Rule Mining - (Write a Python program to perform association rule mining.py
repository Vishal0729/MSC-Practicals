import os
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

base = r"D:/MSC Practicals/Data Science/Practical - 6/"
df = pd.read_excel(os.path.join(base, "Inputs/Online-Retail-Billboard.xlsx"))
output = os.path.join(base, "Outputs/")
os.makedirs(output, exist_ok=True)

# Clean data
df = df.dropna(subset=['InvoiceNo'])
df['InvoiceNo'] = df['InvoiceNo'].astype(str)
df = df[~df['InvoiceNo'].str.contains('C')]
df['Description'] = df['Description'].str.strip()

# Encode as boolean
def rules(country, sup, lift, conf, filename):
    basket = (df[df['Country']==country]
              .groupby(['InvoiceNo','Description'])['Quantity']
              .sum().unstack().fillna(0).astype(bool))  # <-- use boolean here
    
    basket.drop('POSTAGE', axis=1, errors='ignore', inplace=True)

    items = apriori(basket, min_support=sup, use_colnames=True)
    res = association_rules(items, metric="lift", min_threshold=1)
    strong = res[(res.lift >= lift) & (res.confidence >= conf)]
    strong.to_csv(os.path.join(output, filename), index=False)
    return strong

print(rules("France", 0.07, 6, 0.8, "France_Rules.csv"))
print(rules("Germany", 0.05, 4, 0.5, "Germany_Rules.csv"))


