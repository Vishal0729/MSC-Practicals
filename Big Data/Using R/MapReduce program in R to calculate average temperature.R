# ===== GENERATE SAMPLE WEATHER DATASET =====
set.seed(42)

cities <- c("New York", "London", "Tokyo", "Mumbai", "Sydney")
months <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

# Temperature ranges per city (min, max)
temp_ranges <- list(
  "New York" = c(-5, 35),
  "London"   = c(2, 28),
  "Tokyo"    = c(3, 35),
  "Mumbai"   = c(20, 40),
  "Sydney"   = c(10, 38)
)

# Load from CSV file
#weather_data <- read.csv("weather_data.csv", stringsAsFactors = FALSE)
#colnames(weather_data) <- c("city", "month", "temp")
#weather_data$temp <- as.numeric(weather_data$temp)



# library(httr)

# # ===== JUST CHANGE THIS URL =====
# url <- "https://example.com/weather_data.csv"

# # Download and parse
# response <- GET(url)
# text <- content(response, "text", encoding = "UTF-8")
# full_data <- read.csv(text = text, stringsAsFactors = FALSE)

# cat("Columns found:", colnames(full_data), "\n")

# # ===== ADJUST COLUMN NAMES BASED ON YOUR DATASET =====
# # Example columns: City, Month, Year, Temperature, Humidity, WindSpeed
# city_col <- "City"            # Change to your column name
# month_col <- "Month"          # Change to your column name
# temp_col <- "Temperature"     # Change to your column name

# weather_data <- data.frame(
  # city = full_data[[city_col]],
  # month = full_data[[month_col]],
  # temp = as.numeric(full_data[[temp_col]]),
  # stringsAsFactors = FALSE
# )

# Remove rows with NA temperatures
#weather_data <- weather_data[!is.na(weather_data$temp), ]

weather_data <- data.frame(
  city = character(),
  month = character(),
  temp = numeric(),
  stringsAsFactors = FALSE
)

for (city in cities) {
  for (month in months) {
    for (i in 1:3) {
      low <- temp_ranges[[city]][1]
      high <- temp_ranges[[city]][2]
      temp <- round(runif(1, low, high), 1)
      weather_data <- rbind(weather_data, 
                           data.frame(city = city, month = month, 
                                     temp = temp, stringsAsFactors = FALSE))
    }
  }
}

cat(strrep("=", 65), "\n")
cat("   MAPREDUCE: AVERAGE TEMPERATURE FROM WEATHER DATASET\n")
cat(strrep("=", 65), "\n")

cat(sprintf("\nDataset Size: %d records\n", nrow(weather_data)))
cat("Cities:", paste(cities, collapse = ", "), "\n")
cat("Months: 12 (Jan - Dec)\n")
cat("Readings per city per month: 3\n")

cat("\nSample Records (first 10):\n")
cat(sprintf("  %-12s %-6s %10s\n", "CITY", "MONTH", "TEMP (°C)"))
cat(sprintf("  %-12s %-6s %10s\n", strrep("-", 12), strrep("-", 6), strrep("-", 10)))
for (i in 1:10) {
  cat(sprintf("  %-12s %-6s %10.1f\n", 
              weather_data$city[i], weather_data$month[i], weather_data$temp[i]))
}


mapper <- function(record) {
  data.frame(
    key = record$city,
    value = record$temp,
    stringsAsFactors = FALSE
  )
}

shuffle_and_sort <- function(mapped_data) {
  grouped <- split(mapped_data$value, mapped_data$key)
  grouped[order(names(grouped))]
}

reducer <- function(city, temperatures) {
  data.frame(
    city = city,
    avg_temp = round(mean(temperatures), 2),
    min_temp = min(temperatures),
    max_temp = max(temperatures),
    count = length(temperatures),
    stringsAsFactors = FALSE
  )
}

cat("\n", strrep("-", 65), "\n")
cat("[Step 1] MAP Phase\n")
cat(strrep("-", 65), "\n")

mapped_results <- do.call(rbind, lapply(1:nrow(weather_data), function(i) {
  mapper(weather_data[i, ])
}))

cat(sprintf("  Total (city, temperature) pairs emitted: %d\n", nrow(mapped_results)))
cat("\n  Sample mapped output (first 5):\n")
for (i in 1:5) {
  cat(sprintf("    (\"%s\", %.1f)\n", mapped_results$key[i], mapped_results$value[i]))
}


cat("\n", strrep("-", 65), "\n")
cat("[Step 2] SHUFFLE & SORT Phase\n")
cat(strrep("-", 65), "\n")

shuffled <- shuffle_and_sort(mapped_results)
for (city in names(shuffled)) {
  cat(sprintf("  %-12s -> %d temperature readings grouped\n", 
              city, length(shuffled[[city]])))
}


cat("\n", strrep("-", 65), "\n")
cat("[Step 3] REDUCE Phase\n")
cat(strrep("-", 65), "\n")

final_results <- do.call(rbind, lapply(names(shuffled), function(city) {
  temps <- shuffled[[city]]
  result <- reducer(city, temps)
  cat(sprintf("  %-12s: sum(%d readings) / %d = %.2f°C\n", 
              city, length(temps), length(temps), result$avg_temp))
  result
}))

rownames(final_results) <- NULL


cat("\n", strrep("=", 65), "\n")
cat("  FINAL RESULTS: AVERAGE TEMPERATURE BY CITY\n")
cat(strrep("=", 65), "\n")

final_results <- final_results[order(-final_results$avg_temp), ]

cat(sprintf("  %-12s %9s %9s %9s %9s\n", 
            "CITY", "AVG (°C)", "MIN (°C)", "MAX (°C)", "READINGS"))
cat(sprintf("  %-12s %9s %9s %9s %9s\n", 
            strrep("-", 12), strrep("-", 9), strrep("-", 9), 
            strrep("-", 9), strrep("-", 9)))

for (i in seq_len(nrow(final_results))) {
  cat(sprintf("  %-12s %9.2f %9.1f %9.1f %9d\n",
              final_results$city[i], final_results$avg_temp[i],
              final_results$min_temp[i], final_results$max_temp[i],
              final_results$count[i]))
}


# ===== BONUS: AVERAGE TEMPERATURE BY MONTH (All Cities Combined) (CAN BE REMOVED) =====
cat("\n", strrep("=", 65), "\n")
cat("  BONUS: AVERAGE TEMPERATURE BY MONTH (All Cities)\n")
cat(strrep("=", 65), "\n")

mapper_by_month <- function(record) {
  data.frame(key = record$month, value = record$temp, stringsAsFactors = FALSE)
}

mapped_monthly <- do.call(rbind, lapply(1:nrow(weather_data), function(i) {
  mapper_by_month(weather_data[i, ])
}))

shuffled_monthly <- split(mapped_monthly$value, mapped_monthly$key)

cat(sprintf("  %-8s %9s %9s %9s\n", "MONTH", "AVG (°C)", "MIN (°C)", "MAX (°C)"))
cat(sprintf("  %-8s %9s %9s %9s\n", 
            strrep("-", 8), strrep("-", 9), strrep("-", 9), strrep("-", 9)))

for (month in months) {
  temps <- shuffled_monthly[[month]]
  cat(sprintf("  %-8s %9.2f %9.1f %9.1f\n", 
              month, mean(temps), min(temps), max(temps)))
}