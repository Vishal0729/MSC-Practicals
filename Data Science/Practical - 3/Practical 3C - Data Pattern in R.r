############ SAMPLE DATASET (no CSV required) ############
IP_DATA_ALL <- data.frame(
  Country = c("India", "United States", "UK123", "Côte d'Ivoire", "Good Book 101"),
  stringsAsFactors = FALSE
)

############ Extract Unique Country Values ############
unique_countries <- unique(IP_DATA_ALL$Country)

############ Create Pattern Function ############
pattern_convert <- function(text) {
  # Replace letters with A
  text <- gsub("[A-Za-z]", "A", text)
  # Replace numbers with N
  text <- gsub("[0-9]", "N", text)
  # Replace spaces with b
  text <- gsub(" ", "b", text)
  # Replace special characters with u
  text <- gsub("[^ANb]", "u", text)
  return(text)
}

############ Apply Pattern Conversion ############
PatternCountry <- sapply(unique_countries, pattern_convert)

############ Show Results ############
output <- data.frame(Country = unique_countries, Pattern = PatternCountry)
print(output)