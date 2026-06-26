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
library(httr)
library(jsonlite)

# HBase REST API (start with: hbase rest start -p 8080)
base_url <- "http://localhost:8080"

# ===== Step 1: Connect and Check Status =====
cat("Connecting to HBase REST API...\n")
response <- GET(paste0(base_url, "/status/cluster"))
cat("HBase Status:", status_code(response), "\n")

# ===== Step 2: Create Table =====
table_name <- "iot_sensor_data_r"

# Delete if exists
DELETE(paste0(base_url, "/", table_name, "/schema"))

# Create table with column families
schema <- '<?xml version="1.0" encoding="UTF-8"?>
<TableSchema name="iot_sensor_data_r">
  <ColumnSchema name="sensor"/>
  <ColumnSchema name="reading"/>
  <ColumnSchema name="status"/>
</TableSchema>'

response <- PUT(
  paste0(base_url, "/", table_name, "/schema"),
  body = schema,
  content_type("text/xml"),
  add_headers(Accept = "text/xml")
)
cat(sprintf("Table '%s' created: %d\n", table_name, status_code(response)))

# ===== Step 3: Helper Function — Encode values for HBase REST =====
# HBase REST API requires base64 encoding
encode_b64 <- function(text) {
  base64enc::base64encode(charToRaw(text))
}

decode_b64 <- function(encoded) {
  rawToChar(base64enc::base64decode(encoded))
}

# ===== Step 4: Store IoT Sensor Data =====
# install.packages("base64enc") if not installed
library(base64enc)

set.seed(42)
base_time <- as.POSIXct("2024-06-15 00:00:00")
total_records <- 0

sensors <- data.frame(
  id = c("SENSOR_001", "SENSOR_002", "SENSOR_003"),
  type = c("temperature", "humidity", "pressure"),
  location = c("Building_A", "Building_B", "Building_C"),
  stringsAsFactors = FALSE
)

cat("\nStoring IoT sensor data...\n")

for (s in 1:nrow(sensors)) {
  for (i in 1:100) {  # 100 readings per sensor (every 5 min)
    timestamp <- base_time + (i - 1) * 300  # 5 min intervals
    reverse_ts <- as.character(9999999999 - as.numeric(timestamp))
    row_key <- paste0(sensors$id[s], "_", reverse_ts)
    
    # Generate reading
    if (sensors$type[s] == "temperature") {
      value <- round(runif(1, 18, 35), 2)
    } else if (sensors$type[s] == "humidity") {
      value <- round(runif(1, 30, 90), 2)
    } else {
      value <- round(runif(1, 980, 1050), 2)
    }
    
    # Build JSON payload for HBase REST
    payload <- sprintf('{
      "Row": [{
        "key": "%s",
        "Cell": [
          {"column": "%s", "$": "%s"},
          {"column": "%s", "$": "%s"},
          {"column": "%s", "$": "%s"},
          {"column": "%s", "$": "%s"},
          {"column": "%s", "$": "%s"},
          {"column": "%s", "$": "%s"}
        ]
      }]
    }',
      encode_b64(row_key),
      encode_b64("sensor:id"), encode_b64(sensors$id[s]),
      encode_b64("sensor:type"), encode_b64(sensors$type[s]),
      encode_b64("sensor:location"), encode_b64(sensors$location[s]),
      encode_b64("reading:value"), encode_b64(as.character(value)),
      encode_b64("reading:timestamp"), encode_b64(format(timestamp, "%Y-%m-%d %H:%M:%S")),
      encode_b64("status:battery"), encode_b64(as.character(sample(20:100, 1)))
    )
    
    PUT(
      paste0(base_url, "/", table_name, "/", row_key),
      body = payload,
      content_type("application/json"),
      add_headers(Accept = "application/json")
    )
    total_records <- total_records + 1
  }
  cat(sprintf("  %s: 100 records stored\n", sensors$id[s]))
}

cat(sprintf("\nTotal records stored: %d\n", total_records))


# ============================================================
# PART 2: RETRIEVE TIME-SERIES IoT SENSOR DATA
# ============================================================

cat("\n", strrep("=", 60), "\n")
cat("  PART 2: RETRIEVING IoT SENSOR DATA\n")
cat(strrep("=", 60), "\n")

# ===== Step 5: Get Single Row =====
cat("\n[Query 1] Get single record:\n")
row_key <- paste0("SENSOR_001_", as.character(9999999999 - as.numeric(base_time)))
response <- GET(
  paste0(base_url, "/", table_name, "/", row_key),
  add_headers(Accept = "application/json")
)
if (status_code(response) == 200) {
  result <- fromJSON(content(response, "text", encoding = "UTF-8"))
  cells <- result$Row[[1]]$Cell[[1]]
  cat(sprintf("  Row Key: %s\n", row_key))
  for (i in seq_len(nrow(cells))) {
    col <- decode_b64(cells$column[i])
    val <- decode_b64(cells$`$`[i])
    cat(sprintf("    %s: %s\n", col, val))
  }
}

# ===== Step 6: Scan All Data for a Specific Sensor =====
cat("\n[Query 2] Scan SENSOR_001 (first 10 readings):\n")

# Use scanner
scanner_url <- paste0(base_url, "/", table_name, "/scanner")
scanner_body <- '{
  "startRow": "",
  "endRow": "",
  "filter": {
    "type": "PrefixFilter",
    "value": ""
  },
  "batch": 10
}'

# Simple prefix scan using row prefix endpoint
response <- GET(
  paste0(base_url, "/", table_name, "/SENSOR_001*"),
  add_headers(Accept = "application/json"),
  query = list(limit = "10")
)

if (status_code(response) == 200) {
  result <- fromJSON(content(response, "text", encoding = "UTF-8"))
  rows <- result$Row
  
  cat(sprintf("  %-22s %-10s %-8s\n", "TIMESTAMP", "VALUE", "BATTERY"))
  cat(sprintf("  %-22s %-10s %-8s\n", strrep("-", 22), strrep("-", 10), strrep("-", 8)))
  
  for (i in seq_len(min(10, length(rows)))) {
    cells <- rows[[i]]$Cell[[1]]
    ts <- ""
    val <- ""
    bat <- ""
    for (j in seq_len(nrow(cells))) {
      col <- decode_b64(cells$column[j])
      cell_val <- decode_b64(cells$`$`[j])
      if (col == "reading:timestamp") ts <- cell_val
      if (col == "reading:value") val <- cell_val
      if (col == "status:battery") bat <- cell_val
    }
    cat(sprintf("  %-22s %-10s %-8s\n", ts, val, bat))
  }
}

# ===== Step 7: Retrieve by Row Key Range (Time Range) =====
cat("\n[Query 3] Time range query - SENSOR_002 (first hour):\n")

start_time <- as.POSIXct("2024-06-15 00:00:00")
end_time <- as.POSIXct("2024-06-15 01:00:00")

start_key <- paste0("SENSOR_002_", as.character(9999999999 - as.numeric(end_time)))
stop_key <- paste0("SENSOR_002_", as.character(9999999999 - as.numeric(start_time)))

response <- GET(
  paste0(base_url, "/", table_name, "/", start_key, ",", stop_key),
  add_headers(Accept = "application/json")
)

if (status_code(response) == 200) {
  result <- fromJSON(content(response, "text", encoding = "UTF-8"))
  cat("  Time range data retrieved successfully\n")
}

# ===== Step 8: Summary Statistics =====
cat("\n[Query 4] Summary per sensor:\n")
cat(sprintf("  %-12s %-12s %-10s\n", "SENSOR", "TYPE", "RECORDS"))
cat(sprintf("  %-12s %-12s %-10s\n", strrep("-", 12), strrep("-", 12), strrep("-", 10)))

for (s in 1:nrow(sensors)) {
  cat(sprintf("  %-12s %-12s %-10d\n", sensors$id[s], sensors$type[s], 100))
}

# ===== Step 9: Get Latest Readings =====
cat("\n[Query 5] Latest 5 readings for SENSOR_003:\n")
response <- GET(
  paste0(base_url, "/", table_name, "/SENSOR_003*"),
  add_headers(Accept = "application/json"),
  query = list(limit = "5")
)

if (status_code(response) == 200) {
  result <- fromJSON(content(response, "text", encoding = "UTF-8"))
  cat(sprintf("  %-22s %-16s\n", "TIMESTAMP", "PRESSURE (hPa)"))
  cat(sprintf("  %-22s %-16s\n", strrep("-", 22), strrep("-", 16)))
  
  rows <- result$Row
  for (i in seq_len(min(5, length(rows)))) {
    cells <- rows[[i]]$Cell[[1]]
    ts <- ""
    val <- ""
    for (j in seq_len(nrow(cells))) {
      col <- decode_b64(cells$column[j])
      cell_val <- decode_b64(cells$`$`[j])
      if (col == "reading:timestamp") ts <- cell_val
      if (col == "reading:value") val <- cell_val
    }
    cat(sprintf("  %-22s %-16s\n", ts, val))
  }
}

cat("\n", strrep("=", 60), "\n")
cat("  RETRIEVAL COMPLETE!\n")
cat(strrep("=", 60), "\n")