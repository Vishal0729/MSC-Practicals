from collections import defaultdict
import random

# ===== GENERATE SAMPLE WEATHER DATASET =====
# Format: (City, Month, Temperature in °C)
random.seed(42)

cities = ["New York", "London", "Tokyo", "Mumbai", "Sydney"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Temperature ranges per city (min, max)
temp_ranges = {
    "New York": (-5, 35),
    "London": (2, 28),
    "Tokyo": (3, 35),
    "Mumbai": (20, 40),
    "Sydney": (10, 38)
}

'''import csv

# Load from CSV file
weather_data = []
with open("weather_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        city, month, temp = row[0], row[1], float(row[2])
        weather_data.append((city, month, temp))'''
        
        
'''import urllib.request
import csv
from io import StringIO

# ===== JUST CHANGE THIS URL =====
url = "https://example.com/weather_data.csv"

# Download and parse
response = urllib.request.urlopen(url)
text = response.read().decode('utf-8')
reader = csv.reader(StringIO(text))
header = next(reader)  # Skip header row

print("Columns found:", header)

# ===== ADJUST COLUMN INDICES BASED ON YOUR DATASET =====
# Example header: City, Month, Year, Temperature, Humidity, WindSpeed
# If your columns are: [0]=City, [1]=Month, [2]=Year, [3]=Temp, [4]=Humidity
city_col = 0       # Change index based on your CSV
month_col = 1      # Change index based on your CSV
temp_col = 3       # Change index based on your CSV

weather_data = []
for row in reader:
    if len(row) > temp_col:  # Skip empty/malformed rows
        try:
            city = row[city_col].strip()
            month = row[month_col].strip()
            temp = float(row[temp_col])
            weather_data.append((city, month, temp))
        except ValueError:
            continue  # Skip rows with non-numeric temperature'''

weather_data = []
for city in cities:
    for month in months:
        for _ in range(3):
            low, high = temp_ranges[city]
            temp = round(random.uniform(low, high), 1)
            weather_data.append((city, month, temp))

print("=" * 65)
print("   MAPREDUCE: AVERAGE TEMPERATURE FROM WEATHER DATASET")
print("=" * 65)

print(f"\nDataset Size: {len(weather_data)} records")
print(f"Cities: {cities}")
print(f"Months: 12 (Jan - Dec)")
print(f"Readings per city per month: 3")

print("\nSample Records (first 10):")
print(f"  {'CITY':<12} {'MONTH':<6} {'TEMP (°C)':>10}")
print(f"  {'-'*12} {'-'*6} {'-'*10}")
for city, month, temp in weather_data[:10]:
    print(f"  {city:<12} {month:<6} {temp:>10.1f}")

def mapper(record):
    city, month, temp = record
    return (city, temp)

def shuffle_and_sort(mapped_data):
    shuffled = defaultdict(list)
    for key, value in mapped_data:
        shuffled[key].append(value)
    return dict(sorted(shuffled.items()))


def reducer(city, temperatures):
    avg_temp = sum(temperatures) / len(temperatures)
    min_temp = min(temperatures)
    max_temp = max(temperatures)
    count = len(temperatures)
    return (city, round(avg_temp, 2), min_temp, max_temp, count)

print("\n" + "-" * 65)
print("[Step 1] MAP Phase")
print("-" * 65)

mapped_results = []
for record in weather_data:
    mapped_pair = mapper(record)
    mapped_results.append(mapped_pair)

print(f"  Total (city, temperature) pairs emitted: {len(mapped_results)}")
print(f"\n  Sample mapped output (first 5):")
for pair in mapped_results[:5]:
    print(f"    {pair}")

print("\n" + "-" * 65)
print("[Step 2] SHUFFLE & SORT Phase")
print("-" * 65)

shuffled = shuffle_and_sort(mapped_results)
for city, temps in shuffled.items():
    print(f"  {city:<12} -> {len(temps)} temperature readings grouped")

print("\n" + "-" * 65)
print("[Step 3] REDUCE Phase")
print("-" * 65)

final_results = []
for city, temps in shuffled.items():
    result = reducer(city, temps)
    final_results.append(result)
    print(f"  {city:<12}: sum({len(temps)} readings) / {len(temps)} = {result[1]}°C")

print("\n" + "=" * 65)
print("  FINAL RESULTS: AVERAGE TEMPERATURE BY CITY")
print("=" * 65)
print(f"  {'CITY':<12} {'AVG (°C)':>9} {'MIN (°C)':>9} {'MAX (°C)':>9} {'READINGS':>9}")
print(f"  {'-'*12} {'-'*9} {'-'*9} {'-'*9} {'-'*9}")

final_results.sort(key=lambda x: x[1], reverse=True)
for city, avg, mn, mx, count in final_results:
    print(f"  {city:<12} {avg:>9.2f} {mn:>9.1f} {mx:>9.1f} {count:>9}")


# ===== BONUS: AVERAGE TEMPERATURE BY MONTH (All Cities Combined)(CAN BE REMOVED) =====
print("\n" + "=" * 65)
print("  BONUS: AVERAGE TEMPERATURE BY MONTH (All Cities)")
print("=" * 65)


def mapper_by_month(record):
    city, month, temp = record
    return (month, temp)


mapped_monthly = [mapper_by_month(record) for record in weather_data]
shuffled_monthly = defaultdict(list)
for key, value in mapped_monthly:
    shuffled_monthly[key].append(value)

print(f"  {'MONTH':<8} {'AVG (°C)':>9} {'MIN (°C)':>9} {'MAX (°C)':>9}")
print(f"  {'-'*8} {'-'*9} {'-'*9} {'-'*9}")

for month in months:
    temps = shuffled_monthly[month]
    avg = sum(temps) / len(temps)
    print(f"  {month:<8} {avg:>9.2f} {min(temps):>9.1f} {max(temps):>9.1f}")