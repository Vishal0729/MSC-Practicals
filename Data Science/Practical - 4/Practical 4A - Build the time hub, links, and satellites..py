import os, uuid, pandas as pd, sqlite3
from datetime import datetime, timedelta
from pytz import timezone
# Always use this specific Downloads folder for saving DB files
out = r"D:/MSC Practicals/Data Science/Practical - 4/Outputs/"
os.makedirs(out, exist_ok=True)
db1 = os.path.join(out, "Process_Time.db")
db2 = os.path.join(out, "Hub_Time.db")
conn1 = sqlite3.connect(db1)
conn2 = sqlite3.connect(db2)
# Generate datetime list (last 5 days hourly = 120 timestamps — not 10 years)
base = datetime(2018, 1, 1, 0, 0)
dates = [(base - timedelta(hours=i)) for i in range(120)]
rows = []
for d in dates:
    utc = d.replace(tzinfo=timezone('UTC'))
    key = utc.strftime("%Y-%m-%d-%H-%M-%S")
    rows.append([str(uuid.uuid4()), 'UTC', key, utc.strftime("%Y-%m-%d %H:%M:%S")])
df = pd.DataFrame(rows, columns=["ID", "Zone", "DateKey", "DateValue"])
df.set_index("ID", inplace=True)
df.to_sql("Process_Time", conn1, if_exists="replace")
df.to_sql("Hub_Time", conn2, if_exists="replace")
print(" Done! Files saved in Downloads folder as:")
print("Process_Time.db")
print("Hub_Time.db")

