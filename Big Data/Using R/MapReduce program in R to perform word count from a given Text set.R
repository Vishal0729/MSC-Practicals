text_data <- c(
  "Hello world",
  "Hello from the other side",
  "world of MapReduce",
  "MapReduce is powerful"
)

cat(strrep("=", 60), "\n")
cat("     MAPREDUCE WORD COUNT - CUSTOM TEXT DATASET\n")
cat(strrep("=", 60), "\n")
cat("\nInput Data:\n")
for (i in seq_along(text_data)) {
  cat(sprintf("  Line %d: \"%s\"\n", i, text_data[i]))
}


mapper <- function(line) {
  words <- unlist(regmatches(tolower(line), 
                             gregexpr("[a-z]+", tolower(line))))
  data.frame(word = words, count = rep(1L, length(words)), 
             stringsAsFactors = FALSE)
}

shuffle_and_sort <- function(mapped_data) {
  grouped <- split(mapped_data$count, mapped_data$word)
  grouped[order(names(grouped))]
}


reducer <- function(word, counts) {
  data.frame(word = word, count = sum(counts), stringsAsFactors = FALSE)
}

cat("\n", strrep("-", 60), "\n")
cat("[Step 1] MAP Phase\n")
cat(strrep("-", 60), "\n")

mapped_list <- list()
for (i in seq_along(text_data)) {
  mapped <- mapper(text_data[i])
  mapped_list[[i]] <- mapped
  cat(sprintf("  \"%s\"\n", text_data[i]))
  pairs <- paste0("(", mapped$word, ", ", mapped$count, ")", collapse = ", ")
  cat(sprintf("    -> [%s]\n", pairs))
}

all_mapped <- do.call(rbind, mapped_list)
cat(sprintf("\n  Combined mapped output: %d pairs\n", nrow(all_mapped)))


cat("\n", strrep("-", 60), "\n")
cat("[Step 2] SHUFFLE & SORT Phase\n")
cat(strrep("-", 60), "\n")

shuffled <- shuffle_and_sort(all_mapped)
for (word in names(shuffled)) {
  cat(sprintf("  %-15s -> [%s]\n", word, 
              paste(shuffled[[word]], collapse = ", ")))
}

cat("\n", strrep("-", 60), "\n")
cat("[Step 3] REDUCE Phase\n")
cat(strrep("-", 60), "\n")

reduced_list <- list()
for (word in names(shuffled)) {
  counts <- shuffled[[word]]
  result <- reducer(word, counts)
  reduced_list[[word]] <- result
  cat(sprintf("  %-15s: sum([%s]) = %d\n", word, 
              paste(counts, collapse = ", "), result$count))
}

final_results <- do.call(rbind, reduced_list)
rownames(final_results) <- NULL


cat("\n", strrep("=", 60), "\n")
cat("  FINAL WORD COUNT RESULTS\n")
cat(strrep("=", 60), "\n")

final_results <- final_results[order(-final_results$count), ]

cat(sprintf("  %-15s %5s\n", "WORD", "COUNT"))
cat(sprintf("  %-15s %5s\n", strrep("-", 15), strrep("-", 5)))
for (i in seq_len(nrow(final_results))) {
  cat(sprintf("  %-15s %5d\n", final_results$word[i], 
              final_results$count[i]))
}

cat(sprintf("\n  Total unique words: %d\n", nrow(final_results)))
cat(sprintf("  Total word count: %d\n", sum(final_results$count)))