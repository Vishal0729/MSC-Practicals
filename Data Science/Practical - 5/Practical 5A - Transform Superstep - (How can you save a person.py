import pandas as pd, sqlite3, os, uuid
from datetime import datetime
from pytz import timezone

outputs = "D:/MSC Practicals/Data Science/Practical - 5/Outputs/"
os.makedirs(outputs, exist_ok=True)

# ---- Birth info ----
utc_birth = datetime(1960,12,20,10,15,0, tzinfo=timezone('UTC'))
local_birth = utc_birth.astimezone(timezone('Atlantic/Reykjavik'))

# ---- Prepare DataFrames ----
time_df = pd.DataFrame([{
    'IDNumber': str(uuid.uuid4()),
    'ZoneBaseKey': 'UTC',
    'DateTimeKey': utc_birth.strftime("%Y-%m-%d %H:%M:%S"),
    'UTCDateTimeValue': utc_birth,
    'Zone': 'Atlantic/Reykjavik',
    'DateTimeValue': local_birth.strftime("%Y-%m-%d %H:%M:%S")
}])

person_df = pd.DataFrame([{
    'IDNumber': str(uuid.uuid4()),
    'FirstName':'Guðmundur',
    'LastName':'Gunnarsson',
    'Zone':'UTC',
    'DateTimeValue':utc_birth.strftime("%Y-%m-%d %H:%M:%S")
}])

# ---- Save CSV ----
time_df.to_csv(os.path.join(outputs,'Time-Gunnarsson.csv'), index=False)
person_df.to_csv(os.path.join(outputs,'Person-Gunnarsson.csv'), index=False)

# ---- Save to SQLite ----
for db, tables in [(sqlite3.connect(os.path.join(outputs,'5A_datavault.db')), 
                    {'Hub-Time-Gunnarsson': time_df, 'Hub-Person-Gunnarsson': person_df}),
                   (sqlite3.connect(os.path.join(outputs,'5A_datawarehouse.db')), 
                    {'Dim-Time-Gunnarsson': time_df, 'Dim-Person-Gunnarsson': person_df})]:
    for name, df in tables.items():
        df.set_index('IDNumber').to_sql(name, db, if_exists='replace')
    db.close()

print("Done. CSVs and SQLite DBs are in Outputs folder.")

