# Sample data (acting as All_Countries.txt)
data <- data.frame(
  X1 = c("IN","US","UK"),
  X2 = c("India","USA","United Kingdom"),
  X6 = c(111,222,333),
  X7 = c("drop","drop","drop"),
  X8 = c("skip","skip","skip"),
  X9 = c("sample","sample","sample"),
  X12 = c("remove","remove","remove")
)

# Remove (skip) extra columns — logic same as original
clean_data <- subset(data, select = -c(X6, X7, X8, X9, X12))

# Display final cleaned data instead of saving to CSV
print("Cleaned Country Data:")
print(clean_data)

