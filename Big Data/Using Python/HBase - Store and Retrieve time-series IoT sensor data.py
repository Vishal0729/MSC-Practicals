HBase Setup
Bash
# Start HBase
start-hbase.sh

# Start Thrift server (required for Python connection)
hbase thrift start

# Start REST server (required for R connection)
hbase rest start -p 8080

# Verify HBase is running
hbase shell
> status

# Required libraries
# pip install happybase
import happybase
import time
import random
import struct
from datetime import datetime, timedelta

# ===== Step 1: Connect to HBase =====
connection = happybase.Connection('localhost', port=9090)
connection.open()
print("Connected to HBase successfully!")
print("Available tables:", connection.tables())

# ===== Step 2: Create Table for IoT Sensor Data =====
table_name = 'iot_sensor_data'

# Delete table if exists (for fresh start)
if table_name.encode() in connection.tables():
    connection.disable_table(table_name)
    connection.delete_table(table_name)
    print(f"Existing table '{table_name}' deleted.")

# Create table with column families
connection.create_table(
    table_name,
    {
        'sensor': dict(),       # sensor metadata (id, type, location)
        'reading': dict(),      # actual readings (temperature, humidity, pressure)
        'status': dict()        # device status (battery, signal, alert)
    }
)
print(f"Table '{table_name}' created with column families: sensor, reading, status")

# ===== Step 3: Generate and Store IoT Sensor Data =====
table = connection.table(table_name)

# Sensor configurations
sensors = [
    {'id': 'SENSOR_001', 'type': 'temperature', 'location': 'Building_A_Floor1'},
    {'id': 'SENSOR_002', 'type': 'humidity', 'location': 'Building_A_Floor2'},
    {'id': 'SENSOR_003', 'type': 'pressure', 'location': 'Building_B_Floor1'},
    {'id': 'SENSOR_004', 'type': 'temperature', 'location': 'Building_B_Floor2'},
    {'id': 'SENSOR_005', 'type': 'humidity', 'location': 'Building_C_Floor1'},
]

# Generate time-series data (every 5 minutes for 24 hours = 288 readings per sensor)
random.seed(42)
base_time = datetime(2024, 6, 15, 0, 0, 0)
total_records = 0

print("\nStoring IoT sensor data...")
for sensor in sensors:
    for i in range(288):  # 24 hours * 12 readings/hour (every 5 min)
        timestamp = base_time + timedelta(minutes=i * 5)
        
        # Row key: sensor_id + reverse_timestamp (for time-series ordering)
        # Reverse timestamp ensures latest data comes first in scans
        reverse_ts = str(9999999999 - int(timestamp.timestamp()))
        row_key = f"{sensor['id']}_{reverse_ts}"

        # Generate sensor readings based on type
        if sensor['type'] == 'temperature':
            value = round(random.uniform(18.0, 35.0), 2)
            unit = 'celsius'
        elif sensor['type'] == 'humidity':
            value = round(random.uniform(30.0, 90.0), 2)
            unit = 'percent'
        else:
            value = round(random.uniform(980.0, 1050.0), 2)
            unit = 'hPa'

        # Store data in HBase
        table.put(row_key.encode(), {
            b'sensor:id': sensor['id'].encode(),
            b'sensor:type': sensor['type'].encode(),
            b'sensor:location': sensor['location'].encode(),
            b'reading:value': str(value).encode(),
            b'reading:unit': unit.encode(),
            b'reading:timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S').encode(),
            b'status:battery': str(random.randint(20, 100)).encode(),
            b'status:signal': str(random.randint(60, 100)).encode(),
            b'status:alert': str(value > 32 or value < 20).encode()
        })
        total_records += 1

print(f"Total records stored: {total_records}")
print(f"Records per sensor: 288 (every 5 min for 24 hours)")

# ===== Step 4: Store using Batch (Faster method) =====
print("\nStoring additional batch data...")
batch_sensor = {'id': 'SENSOR_006', 'type': 'temperature', 'location': 'Building_D'}
batch = table.batch()

for i in range(100):
    timestamp = base_time + timedelta(minutes=i * 5)
    reverse_ts = str(9999999999 - int(timestamp.timestamp()))
    row_key = f"SENSOR_006_{reverse_ts}"
    value = round(random.uniform(20.0, 30.0), 2)
    
    batch.put(row_key.encode(), {
        b'sensor:id': b'SENSOR_006',
        b'sensor:type': b'temperature',
        b'sensor:location': b'Building_D',
        b'reading:value': str(value).encode(),
        b'reading:timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S').encode(),
        b'status:battery': str(random.randint(50, 100)).encode(),
    })

batch.send()
print("Batch insert complete! (100 records for SENSOR_006)")

# ===== Step 5: Verify Storage =====
print(f"\nTotal rows in table: ~{total_records + 100}")
print("\nSample stored record:")
for key, data in table.scan(limit=1):
    print(f"  Row Key: {key.decode()}")
    for col, val in data.items():
        print(f"    {col.decode()}: {val.decode()}")


# ============================================================
# PART 2: RETRIEVE TIME-SERIES IoT SENSOR DATA (5 Marks)
# ============================================================

print("\n" + "="*60)
print("  PART 2: RETRIEVING IoT SENSOR DATA")
print("="*60)

# ===== Step 6: Get Single Row =====
print("\n[Query 1] Get single record by row key:")
row_key = f"SENSOR_001_{str(9999999999 - int(base_time.timestamp()))}"
row = table.row(row_key.encode())
if row:
    print(f"  Row Key: {row_key}")
    for col, val in row.items():
        print(f"    {col.decode()}: {val.decode()}")

# ===== Step 7: Scan All Data for a Specific Sensor =====
print("\n[Query 2] All readings for SENSOR_001 (first 10):")
print(f"  {'TIMESTAMP':<22} {'VALUE':<10} {'BATTERY':<8}")
print(f"  {'-'*22} {'-'*10} {'-'*8}")

count = 0
for key, data in table.scan(row_prefix=b'SENSOR_001'):
    if count >= 10:
        break
    ts = data.get(b'reading:timestamp', b'N/A').decode()
    val = data.get(b'reading:value', b'N/A').decode()
    bat = data.get(b'status:battery', b'N/A').decode()
    print(f"  {ts:<22} {val:<10} {bat:<8}")
    count += 1

# ===== Step 8: Scan with Row Key Range (Time Range Query) =====
print("\n[Query 3] Time range query - SENSOR_002 (06:00 to 08:00):")

start_time = datetime(2024, 6, 15, 6, 0, 0)
end_time = datetime(2024, 6, 15, 8, 0, 0)

# Reverse timestamps for range
start_key = f"SENSOR_002_{str(9999999999 - int(end_time.timestamp()))}"
stop_key = f"SENSOR_002_{str(9999999999 - int(start_time.timestamp()))}"

print(f"  {'TIMESTAMP':<22} {'HUMIDITY %':<12}")
print(f"  {'-'*22} {'-'*12}")

for key, data in table.scan(row_start=start_key.encode(), row_stop=stop_key.encode()):
    ts = data.get(b'reading:timestamp', b'').decode()
    val = data.get(b'reading:value', b'').decode()
    print(f"  {ts:<22} {val:<12}")

# ===== Step 9: Filter by Column Value =====
print("\n[Query 4] Readings with alert=True (high/low readings):")
print(f"  {'SENSOR':<12} {'TIMESTAMP':<22} {'VALUE':<10} {'ALERT':<6}")
print(f"  {'-'*12} {'-'*22} {'-'*10} {'-'*6}")

count = 0
for key, data in table.scan():
    alert = data.get(b'status:alert', b'False').decode()
    if alert == 'True' and count < 10:
        sensor_id = data.get(b'sensor:id', b'').decode()
        ts = data.get(b'reading:timestamp', b'').decode()
        val = data.get(b'reading:value', b'').decode()
        print(f"  {sensor_id:<12} {ts:<22} {val:<10} {alert:<6}")
        count += 1

# ===== Step 10: Retrieve Data by Location =====
print("\n[Query 5] All sensors in Building_A_Floor1:")
print(f"  {'SENSOR':<12} {'TYPE':<12} {'TIMESTAMP':<22} {'VALUE':<10}")
print(f"  {'-'*12} {'-'*12} {'-'*22} {'-'*10}")

count = 0
for key, data in table.scan(row_prefix=b'SENSOR_001'):
    location = data.get(b'sensor:location', b'').decode()
    if location == 'Building_A_Floor1' and count < 10:
        sensor_id = data.get(b'sensor:id', b'').decode()
        s_type = data.get(b'sensor:type', b'').decode()
        ts = data.get(b'reading:timestamp', b'').decode()
        val = data.get(b'reading:value', b'').decode()
        print(f"  {sensor_id:<12} {s_type:<12} {ts:<22} {val:<10}")
        count += 1

# ===== Step 11: Aggregate Query — Average per Sensor =====
print("\n[Query 6] Average reading per sensor:")
print(f"  {'SENSOR':<12} {'TYPE':<12} {'AVG VALUE':<12} {'READINGS':<10}")
print(f"  {'-'*12} {'-'*12} {'-'*12} {'-'*10}")

for sensor in sensors:
    values = []
    for key, data in table.scan(row_prefix=sensor['id'].encode()):
        val = data.get(b'reading:value', b'0').decode()
        values.append(float(val))
    if values:
        avg_val = sum(values) / len(values)
        print(f"  {sensor['id']:<12} {sensor['type']:<12} {avg_val:<12.2f} {len(values):<10}")

# ===== Step 12: Retrieve Latest N Readings =====
print("\n[Query 7] Latest 5 readings for SENSOR_003:")
print(f"  {'TIMESTAMP':<22} {'PRESSURE (hPa)':<16}")
print(f"  {'-'*22} {'-'*16}")

count = 0
for key, data in table.scan(row_prefix=b'SENSOR_003'):
    if count >= 5:
        break
    ts = data.get(b'reading:timestamp', b'').decode()
    val = data.get(b'reading:value', b'').decode()
    print(f"  {ts:<22} {val:<16}")
    count += 1

# ===== Step 13: Close Connection =====
connection.close()
print("\nHBase connection closed.")