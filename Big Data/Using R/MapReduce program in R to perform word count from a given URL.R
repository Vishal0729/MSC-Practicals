library(httr)

url <- "https://www.gutenberg.org/files/1342/1342-0.txt"
response <- GET(url)
text <- content(response, "text", encoding = "UTF-8")

lines <- unlist(strsplit(text, "\n"))
cat("Total lines downloaded:", length(lines), "\n")


mapper <- function(line) {
  words <- unlist(regmatches(tolower(line), 
                             gregexpr("[a-z]+", tolower(line))))
  if (length(words) == 0) return(data.frame(word = character(0), 
                                             count = integer(0)))
  data.frame(word = words, count = rep(1L, length(words)), 
             stringsAsFactors = FALSE)
}


shuffle_and_sort <- function(mapped_data) {
  split(mapped_data$count, mapped_data$word)
}


reducer <- function(word, counts) {
  data.frame(word = word, count = sum(counts), stringsAsFactors = FALSE)
}


cat("\n", strrep("=", 60), "\n")
cat("         MAPREDUCE WORD COUNT - GUTENBERG DATASET\n")
cat(strrep("=", 60), "\n")

cat("\n[Step 1] MAP Phase - Processing lines...\n")
mapped_results <- do.call(rbind, lapply(lines, mapper))
cat("  Total (word, 1) pairs emitted:", nrow(mapped_results), "\n")

cat("\n[Step 2] SHUFFLE & SORT Phase - Grouping by key...\n")
shuffled_data <- shuffle_and_sort(mapped_results)
cat("  Unique words found:", length(shuffled_data), "\n")

cat("\n[Step 3] REDUCE Phase - Aggregating counts...\n")
reduced_results <- do.call(rbind, mapply(reducer, 
                                          names(shuffled_data), 
                                          shuffled_data, 
                                          SIMPLIFY = FALSE))

reduced_results <- reduced_results[order(-reduced_results$count), ]
rownames(reduced_results) <- NULL

cat("\n", strrep("-", 40), "\n")
cat("  TOP 25 MOST FREQUENT WORDS\n")
cat(strrep("-", 40), "\n")
cat(sprintf("  %-20s %10s\n", "WORD", "COUNT"))
cat(sprintf("  %-20s %10s\n", "----", "-----"))
for (i in 1:25) {
  cat(sprintf("  %-20s %10d\n", reduced_results$word[i], 
              reduced_results$count[i]))
}

cat(sprintf("\n  Total unique words: %d\n", nrow(reduced_results)))
cat(sprintf("  Total word occurrences: %d\n", sum(reduced_results$count)))