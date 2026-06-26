# Required libraries
# pip install pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max, min, sum, when, round as spark_round
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType

# ===== Step 1: Create Spark Session =====
spark = SparkSession.builder \
    .appName("CSV Processing with PySpark") \
    .master("local[*]") \
    .getOrCreate()

print("Spark Session created successfully!")
print(f"Spark Version: {spark.version}")

# ===== Step 2: Read CSV Dataset =====
url = "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"

# Download file first (PySpark reads local/HDFS files)
import urllib.request
urllib.request.urlretrieve(url, "hw_200.csv")

# --- If file is already downloaded locally: ---
# (just skip the download step above)
# -----------------------------------------------

# Read CSV with header and infer schema
df = spark.read.csv("hw_200.csv", header=True, inferSchema=True)

# Rename columns (remove quotes/spaces if any)
df = df.toDF("Index", "Height_Inches", "Weight_Pounds")

print("\n===== DATASET LOADED =====")
print(f"Rows: {df.count()}, Columns: {len(df.columns)}")

# ===== Step 3: Display Schema and Sample Data =====
print("\nSchema:")
df.printSchema()

print("\nFirst 10 rows:")
df.show(10)

# ===== Step 4: Basic Statistics =====
print("\nDescriptive Statistics:")
df.describe().show()

# ===== Step 5: Data Processing — Add New Columns =====
# Convert height to cm, weight to kg
df = df.withColumn("Height_CM", spark_round(col("Height_Inches") * 2.54, 2))
df = df.withColumn("Weight_KG", spark_round(col("Weight_Pounds") * 0.4536, 2))

# Calculate BMI = weight(kg) / height(m)^2
df = df.withColumn("Height_M", col("Height_CM") / 100)
df = df.withColumn("BMI", spark_round(col("Weight_KG") / (col("Height_M") ** 2), 2))

# Categorize BMI
df = df.withColumn("BMI_Category",
    when(col("BMI") < 18.5, "Underweight")
    .when(col("BMI") < 25, "Normal")
    .when(col("BMI") < 30, "Overweight")
    .otherwise("Obese"))

print("\nProcessed Data (with new columns):")
df.show(10)

# ===== Step 6: FILTERING Operations =====
print("\n" + "="*60)
print("  FILTERING OPERATIONS")
print("="*60)

# Filter 1: Height > 70 inches
print("\n[Filter 1] People taller than 70 inches:")
tall_people = df.filter(col("Height_Inches") > 70)
tall_people.show(5)
print(f"  Count: {tall_people.count()}")

# Filter 2: Weight between 140 and 160 pounds
print("\n[Filter 2] Weight between 140-160 pounds:")
medium_weight = df.filter((col("Weight_Pounds") >= 140) & (col("Weight_Pounds") <= 160))
medium_weight.show(5)
print(f"  Count: {medium_weight.count()}")

# Filter 3: BMI Category = Overweight
print("\n[Filter 3] Overweight people (BMI 25-30):")
overweight = df.filter(col("BMI_Category") == "Overweight")
overweight.show(5)
print(f"  Count: {overweight.count()}")

# Filter 4: Multiple conditions - Tall AND Heavy
print("\n[Filter 4] Tall (>68 inches) AND Heavy (>170 pounds):")
tall_heavy = df.filter((col("Height_Inches") > 68) & (col("Weight_Pounds") > 170))
tall_heavy.show(5)
print(f"  Count: {tall_heavy.count()}")

# ===== Step 7: SUMMARIZING Operations =====
print("\n" + "="*60)
print("  SUMMARIZING OPERATIONS")
print("="*60)

# Summary 1: Overall Averages
print("\n[Summary 1] Overall Averages:")
df.select(
    spark_round(avg("Height_Inches"), 2).alias("Avg_Height_Inches"),
    spark_round(avg("Weight_Pounds"), 2).alias("Avg_Weight_Pounds"),
    spark_round(avg("BMI"), 2).alias("Avg_BMI")
).show()

# Summary 2: Min, Max, Count
print("[Summary 2] Min, Max values:")
df.select(
    min("Height_Inches").alias("Min_Height"),
    max("Height_Inches").alias("Max_Height"),
    min("Weight_Pounds").alias("Min_Weight"),
    max("Weight_Pounds").alias("Max_Weight"),
    min("BMI").alias("Min_BMI"),
    max("BMI").alias("Max_BMI")
).show()

# Summary 3: Group by BMI Category
print("[Summary 3] Statistics by BMI Category:")
df.groupBy("BMI_Category") \
    .agg(
        count("*").alias("Count"),
        spark_round(avg("Height_Inches"), 2).alias("Avg_Height"),
        spark_round(avg("Weight_Pounds"), 2).alias("Avg_Weight"),
        spark_round(avg("BMI"), 2).alias("Avg_BMI")
    ) \
    .orderBy("Avg_BMI") \
    .show()

# Summary 4: Height distribution (bins)
print("[Summary 4] Height Distribution:")
df.withColumn("Height_Group",
    when(col("Height_Inches") < 64, "Short (<64)")
    .when(col("Height_Inches") < 68, "Medium (64-68)")
    .when(col("Height_Inches") < 72, "Tall (68-72)")
    .otherwise("Very Tall (>72)")) \
    .groupBy("Height_Group") \
    .agg(count("*").alias("Count"), spark_round(avg("Weight_Pounds"), 2).alias("Avg_Weight")) \
    .orderBy("Height_Group") \
    .show()

# Summary 5: Percentiles
print("[Summary 5] Percentiles:")
quantiles = df.approxQuantile("BMI", [0.25, 0.5, 0.75], 0.01)
print(f"  BMI 25th percentile: {quantiles[0]:.2f}")
print(f"  BMI 50th percentile: {quantiles[1]:.2f}")
print(f"  BMI 75th percentile: {quantiles[2]:.2f}")

# ===== Step 8: SQL Queries on DataFrame =====
print("\n" + "="*60)
print("  SQL QUERIES (Using Spark SQL)")
print("="*60)

# Register as temporary view
df.createOrReplaceTempView("people")

# SQL Query 1
print("\n[SQL 1] Top 5 heaviest people:")
spark.sql("""
    SELECT Index, Height_Inches, Weight_Pounds, BMI, BMI_Category
    FROM people
    ORDER BY Weight_Pounds DESC
    LIMIT 5
""").show()

# SQL Query 2
print("[SQL 2] Average BMI by category:")
spark.sql("""
    SELECT BMI_Category, COUNT(*) as Count,
           ROUND(AVG(BMI), 2) as Avg_BMI,
           ROUND(AVG(Weight_Pounds), 2) as Avg_Weight
    FROM people
    GROUP BY BMI_Category
    ORDER BY Avg_BMI
""").show()

# SQL Query 3
print("[SQL 3] People with BMI > 28:")
spark.sql("""
    SELECT Index, Height_Inches, Weight_Pounds, BMI
    FROM people
    WHERE BMI > 28
    ORDER BY BMI DESC
""").show(5)

# ===== Step 9: Save Processed Data =====
# Save as CSV
df.write.csv("processed_hw_200", header=True, mode="overwrite")
print("\nProcessed data saved to 'processed_hw_200/' folder")

# ===== Step 10: Stop Spark Session =====
spark.stop()
print("\nSpark Session stopped.")