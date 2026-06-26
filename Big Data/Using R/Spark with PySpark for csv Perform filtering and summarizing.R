# Required libraries
# install.packages("sparklyr")
library(sparklyr)
library(dplyr)

# ===== Step 1: Create Spark Connection =====
# Install Spark locally (one-time)
# spark_install(version = "3.3")

sc <- spark_connect(master = "local")
cat("Spark Session created successfully!\n")
cat("Spark Version:", spark_version(sc), "\n")

# ===== Step 2: Read CSV Dataset =====
url <- "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"
download.file(url, "hw_200.csv")

# --- If file is already downloaded locally: ---
# (just skip the download step above)
# -----------------------------------------------

# Read into Spark DataFrame
df <- spark_read_csv(sc, name = "people", path = "hw_200.csv", header = TRUE, infer_schema = TRUE)

# Rename columns
df <- df %>% rename(Index = 1, Height_Inches = 2, Weight_Pounds = 3)

cat("\n===== DATASET LOADED =====\n")
cat(sprintf("Rows: %d, Columns: %d\n", sdf_nrow(df), ncol(df)))

# ===== Step 3: Display Schema and Sample Data =====
cat("\nSchema:\n")
glimpse(df)

cat("\nFirst 10 rows:\n")
print(head(df, 10))

# ===== Step 4: Basic Statistics =====
cat("\nDescriptive Statistics:\n")
print(sdf_describe(df))

# ===== Step 5: Data Processing — Add New Columns =====
df <- df %>%
  mutate(
    Height_CM = round(Height_Inches * 2.54, 2),
    Weight_KG = round(Weight_Pounds * 0.4536, 2),
    Height_M = Height_Inches * 2.54 / 100,
    BMI = round(Weight_KG / (Height_M^2), 2),
    BMI_Category = case_when(
      BMI < 18.5 ~ "Underweight",
      BMI < 25 ~ "Normal",
      BMI < 30 ~ "Overweight",
      TRUE ~ "Obese"
    )
  )

cat("\nProcessed Data (with new columns):\n")
print(head(df, 10))

# ===== Step 6: FILTERING Operations =====
cat("\n", strrep("=", 60), "\n")
cat("  FILTERING OPERATIONS\n")
cat(strrep("=", 60), "\n")

# Filter 1: Height > 70 inches
cat("\n[Filter 1] People taller than 70 inches:\n")
tall_people <- df %>% filter(Height_Inches > 70)
print(head(tall_people, 5))
cat(sprintf("  Count: %d\n", sdf_nrow(tall_people)))

# Filter 2: Weight between 140-160
cat("\n[Filter 2] Weight between 140-160 pounds:\n")
medium_weight <- df %>% filter(Weight_Pounds >= 140, Weight_Pounds <= 160)
print(head(medium_weight, 5))
cat(sprintf("  Count: %d\n", sdf_nrow(medium_weight)))

# Filter 3: Overweight
cat("\n[Filter 3] Overweight people (BMI 25-30):\n")
overweight <- df %>% filter(BMI_Category == "Overweight")
print(head(overweight, 5))
cat(sprintf("  Count: %d\n", sdf_nrow(overweight)))

# Filter 4: Tall AND Heavy
cat("\n[Filter 4] Tall (>68) AND Heavy (>170):\n")
tall_heavy <- df %>% filter(Height_Inches > 68, Weight_Pounds > 170)
print(head(tall_heavy, 5))
cat(sprintf("  Count: %d\n", sdf_nrow(tall_heavy)))

# ===== Step 7: SUMMARIZING Operations =====
cat("\n", strrep("=", 60), "\n")
cat("  SUMMARIZING OPERATIONS\n")
cat(strrep("=", 60), "\n")

# Summary 1: Overall Averages
cat("\n[Summary 1] Overall Averages:\n")
overall <- df %>%
  summarise(
    Avg_Height = round(mean(Height_Inches), 2),
    Avg_Weight = round(mean(Weight_Pounds), 2),
    Avg_BMI = round(mean(BMI), 2)
  )
print(collect(overall))

# Summary 2: Min, Max
cat("\n[Summary 2] Min, Max values:\n")
min_max <- df %>%
  summarise(
    Min_Height = min(Height_Inches), Max_Height = max(Height_Inches),
    Min_Weight = min(Weight_Pounds), Max_Weight = max(Weight_Pounds),
    Min_BMI = min(BMI), Max_BMI = max(BMI)
  )
print(collect(min_max))

# Summary 3: Group by BMI Category
cat("\n[Summary 3] Statistics by BMI Category:\n")
bmi_summary <- df %>%
  group_by(BMI_Category) %>%
  summarise(
    Count = n(),
    Avg_Height = round(mean(Height_Inches), 2),
    Avg_Weight = round(mean(Weight_Pounds), 2),
    Avg_BMI = round(mean(BMI), 2)
  ) %>%
  arrange(Avg_BMI)
print(collect(bmi_summary))

# Summary 4: Height distribution
cat("\n[Summary 4] Height Distribution:\n")
height_dist <- df %>%
  mutate(Height_Group = case_when(
    Height_Inches < 64 ~ "Short (<64)",
    Height_Inches < 68 ~ "Medium (64-68)",
    Height_Inches < 72 ~ "Tall (68-72)",
    TRUE ~ "Very Tall (>72)"
  )) %>%
  group_by(Height_Group) %>%
  summarise(Count = n(), Avg_Weight = round(mean(Weight_Pounds), 2)) %>%
  arrange(Height_Group)
print(collect(height_dist))

# ===== Step 8: SQL Queries =====
cat("\n", strrep("=", 60), "\n")
cat("  SQL QUERIES (Using Spark SQL)\n")
cat(strrep("=", 60), "\n")

# SQL Query 1: Top 5 heaviest
cat("\n[SQL 1] Top 5 heaviest people:\n")
result1 <- sdf_sql(sc, "
    SELECT Index, Height_Inches, Weight_Pounds, BMI, BMI_Category
    FROM people
    ORDER BY Weight_Pounds DESC
    LIMIT 5
")
print(collect(result1))

# SQL Query 2: AVG by category
cat("\n[SQL 2] Average BMI by category:\n")
# Need to register updated df
sdf_register(df, "people_processed")
result2 <- sdf_sql(sc, "
    SELECT BMI_Category, COUNT(*) as Count,
           ROUND(AVG(BMI), 2) as Avg_BMI
    FROM people_processed
    GROUP BY BMI_Category
    ORDER BY Avg_BMI
")
print(collect(result2))

# ===== Step 9: Save Processed Data =====
spark_write_csv(df, "processed_hw_200", header = TRUE, mode = "overwrite")
cat("\nProcessed data saved.\n")

# ===== Step 10: Disconnect Spark =====
spark_disconnect(sc)
cat("\nSpark Session disconnected.\n")