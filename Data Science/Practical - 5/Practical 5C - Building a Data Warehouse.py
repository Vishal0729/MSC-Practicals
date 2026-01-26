import pandas as pd, sqlite3, os, uuid
from datetime import datetime
from pytz import timezone

# Base folder
Base = "D:/MSC Practicals/Data Science/Practical - 5/Outputs/"
os.makedirs(Base, exist_ok=True)

# ---- Birth info ----
utc_birth = datetime(1960,12,20,10,15,0, tzinfo=timezone('UTC'))
zones = ['UTC', 'Atlantic/Reykjavik', 'Europe/London']

# ---- Time Dimension ----
time_df = pd.DataFrame([{
    'TimeID': str(uuid.uuid4()),
    'UTCDate': utc_birth.strftime("%Y-%m-%d %H:%M:%S"),
    'LocalTime': utc_birth.astimezone(timezone(z)).strftime("%Y-%m-%d %H:%M:%S"),
    'TimeZone': z
} for z in zones])
time_df.to_csv(os.path.join(Base,'Dim-Time.csv'), index=False)

# ---- Person Dimension ----
person_df = pd.DataFrame([{
    'PersonID': str(uuid.uuid4()),
    'FirstName':'Guðmundur',
    'SecondName':'',
    'LastName':'Gunnarsson',
    'BirthDate': utc_birth.strftime("%Y-%m-%d %H:%M:%S"),
    'Zone':'UTC'
}])
person_df.to_csv(os.path.join(Base,'Dim-Person.csv'), index=False)

# ---- Fact table ----
fact_df = pd.DataFrame([{
    'FactID': str(uuid.uuid4()),
    'PersonID': person_df['PersonID'][0],
    'TimeID': time_df['TimeID'][0]
}])
fact_df.to_csv(os.path.join(Base,'Fact-Person-Time.csv'), index=False)

# ---- Save to SQLite ----
for db_name, tables in [('datavault.db', [time_df, person_df, fact_df]),
                        ('datawarehouse.db', [time_df, person_df, fact_df])]:
    db = sqlite3.connect(os.path.join(Base, db_name))
    db.execute("PRAGMA foreign_keys=ON")
    time_df.set_index('TimeID').to_sql('Dim-Time', db, if_exists='replace')
    person_df.set_index('PersonID').to_sql('Dim-Person', db, if_exists='replace')
    fact_df.set_index('FactID').to_sql('Fact-Person-Time', db, if_exists='replace')
    db.close()

print("Done. CSVs and SQLite DBs are in Base folder.")
