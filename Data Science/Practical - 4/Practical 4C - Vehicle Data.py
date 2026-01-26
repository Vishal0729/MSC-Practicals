import os, uuid, pandas as pd, sqlite3

dl = r"D:/MSC Practicals/Data Sceince/Practical - 4/"
df = pd.read_csv(os.path.join(dl, "Inputs/VehicleData.csv"))

u = df[['Make','Model']].drop_duplicates()
u['ObjectType'] = 'vehicle'
u['ObjectUUID'] = [str(uuid.uuid4()) for _ in range(len(u))]
u['ObjectKey'] = u.apply(lambda r: f"({r.Make.lower().replace(' ','-')})-({r.Model.lower().replace(' ','-')})", axis=1)

pdb = sqlite3.connect(os.path.join(dl, "Outputs/Process_Vehicles.db"))
vdb = sqlite3.connect(os.path.join(dl, "Outputs/DataVault_Vehicles.db"))

df.to_sql("Process_Vehicles", pdb, if_exists="replace")
u[['ObjectType','ObjectKey','ObjectUUID']].to_sql("Hub_Object_Vehicle", vdb, if_exists="replace")
u[['ObjectType','ObjectKey','ObjectUUID','Make','Model']].to_sql("Satellite_Object_Make_Model", vdb, if_exists="replace")

vdb.execute("""CREATE VIEW IF NOT EXISTS Dim_Object AS
SELECT H.ObjectType, H.ObjectKey, S.Make AS VehicleMake, S.Model AS VehicleModel
FROM Hub_Object_Vehicle H JOIN Satellite_Object_Make_Model S USING (ObjectUUID)""")

print("Done! Data Vault created in Outputs.")



