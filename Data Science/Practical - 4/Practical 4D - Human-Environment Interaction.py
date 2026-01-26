import pandas as pd, sqlite3, uuid, os

out = r"D:/MSC Practicals/Data Science/Practical - 4/"
db = os.path.join(out, "Outputs/LocationData.db")

rows = []
for lon in range(-180, 180, 10):
    for lat in range(-90, 90, 10):
        rows.append({
            "ID": str(uuid.uuid4()),
            "LocationName": f"L{lon*1000:+07d}-{lat*1000:+07d}",
            "Longitude": lon,
            "Latitude": lat
        })

df = pd.DataFrame(rows)
conn = sqlite3.connect(db)
df.to_sql("Process_Location", conn, if_exists="replace")
df.to_sql("Hub_Location", conn, if_exists="replace")
print("DONE — Location database created in Outputs")

