import pandas as pd
from geopy.distance import geodesic
import os
# Paths
Base = r"D:/MSC Practicals/Data Science/Practical - 3/"
input_file = f"{Base}/Inputs/GB_Postcode_Warehouse.csv"
# Load & clean
df = pd.read_csv(input_file)
df = df[(df.latitude != 0) & (df.longitude != 0)].drop_duplicates(subset='postcode')
# Output folder
os.makedirs(Base, exist_ok=True)
# Loop over first 20 warehouses (sellers)
for I, seller in df.head(20).iterrows():
    routes = df.copy()
    routes['Seller'] = f"WH-{seller.postcode}"
    routes['Seller_Latitude'] = seller.latitude
    routes['Seller_Longitude'] = seller.longitude
    routes['Buyer'] = 'WH-' + routes['postcode']
    routes['Buyer_Latitude'] = routes['latitude']
    routes['Buyer_Longitude'] = routes['longitude']
    routes['Distance'] = routes.apply(
        lambda r: round(geodesic((seller.latitude, seller.longitude),
                                  (r.latitude, r.longitude)).miles, 6), axis=1
    )
    # Drop unnecessary columns
    routes = routes.drop(columns=['id', 'postcode', 'latitude', 'longitude'])
    # Save route CSV
    routes.to_csv(f"{Base}/Outputs/Retrieve_Route_WH-{seller.postcode}_Route.csv", index=False)
print("Delivery routes generated successfully!")
