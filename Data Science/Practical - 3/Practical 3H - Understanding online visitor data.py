import os, pandas as pd, gzip

# Load data -> remove duplicates ->      export in CSV, JSON, and compressed formats
input = r"D:/MSC Practicals/Data Science/Practical - 3/Inputs/IP_DATA_ALL.csv"
out = r"D:/MSC Practicals/Data Science/Practical - 3/Outputs"
os.makedirs(out, exist_ok=True)

cols = ['ID','Country','Place.Name','Post.Code','Latitude','Longitude','First.IP.Number','Last.IP.Number']
df = pd.read_csv(input, usecols=cols, dtype=str, low_memory=False).drop_duplicates()
df10 = df.head(10)

df.to_csv(f"{out}/Retrieve_Online_Visitor.csv", index=False)
df10.to_csv(f"{out}/Retrieve_Online_Visitor_10.csv", index=False)

for c in ['gzip','bz2','xz']:
    df.to_csv(f"{out}/Retrieve_Online_Visitor.csv" + ('.gz' if c=='gzip' else f".{c}"), index=False, compression=c)

for o in ['split','records','index','columns','values','table']:
    j = f"{out}/Retrieve_Online_Visitor_{o}.json"
    df.to_json(j, orient=o)
    df10.to_json(f"{out}/Retrieve_Online_Visitor_10_{o}.json", orient=o)

    with open(j, "rb") as fi, gzip.open(j + ".gz", "wb") as fo: fo.write(fi.read())
    with gzip.open(j + ".gz", "rb") as fi, open(j.replace(".json","_UnGZip.json"), "wb") as fo: fo.write(fi.read())

print("All files created successfully!")

