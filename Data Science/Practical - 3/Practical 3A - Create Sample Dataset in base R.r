# Create a sample dataset in base R
IP_DATA_ALL <- data.frame(
  Country = c("US", "GB", "US", "DE", "GB"),
  Place.Name = c("New York", "London", "Los Angeles", "Berlin", "Manchester"),
  Post.Code = c(10001, 12345, 90001, 10115, 54321),
  Latitude = c(40.7128, 51.5092, 34.0522, 52.5200, 53.4808),
  Longitude = c(-74.0060, -0.1180, -118.2437, 13.4050, -2.2426),
  stringsAsFactors = FALSE
)

# View the data
print(IP_DATA_ALL)

# Calculate mean latitude by Country and Place.Name
MeanData <- aggregate(Latitude ~ Country + Place.Name, data = IP_DATA_ALL, FUN = mean)

print(MeanData)