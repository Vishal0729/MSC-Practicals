# Required libraries
library(tidytext)    # Text mining
library(dplyr)       # Data manipulation
library(ggplot2)     # Plotting
library(stringr)     # String operations

# ===== Step 1: Load the Sentiment140 Dataset =====
url <- "https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv"
df <- read.csv(url, header = FALSE, stringsAsFactors = FALSE, encoding = "latin1")
colnames(df) <- c("target", "id", "date", "flag", "user", "text")

# --- If file is downloaded locally (from Kaggle), use this instead: ---
# df <- read.csv("training.1600000.processed.noemoticon.csv",
#                header = FALSE, stringsAsFactors = FALSE, encoding = "latin1")
# colnames(df) <- c("target", "id", "date", "flag", "user", "text")
# ----------------------------------------------------------------------

cat("Dataset shape:", nrow(df), "x", ncol(df), "\n")
cat("\nTarget distribution (0=Negative, 4=Positive):\n")
print(table(df$target))

# ===== Step 2: Sample and Preprocess =====
set.seed(42)
df_sample <- df[sample(1:nrow(df), 20000), ]
cat(sprintf("\nWorking with sample: %d tweets\n", nrow(df_sample)))

# Map labels
df_sample$sentiment <- ifelse(df_sample$target == 0, "Negative", "Positive")

# Text cleaning function
clean_text <- function(text) {
  text <- tolower(text)
  text <- str_replace_all(text, "http\\S+|www\\S+", "")    # Remove URLs
  text <- str_replace_all(text, "@\\w+", "")                # Remove mentions
  text <- str_replace_all(text, "#\\w+", "")                # Remove hashtags
  text <- str_replace_all(text, "rt\\s+", "")               # Remove RT
  text <- str_replace_all(text, "[^a-zA-Z\\s]", "")         # Remove special chars
  text <- str_replace_all(text, "\\s+", " ")                # Remove extra spaces
  trimws(text)
}

cat("\nCleaning text data...\n")
df_sample$clean_text <- sapply(df_sample$text, clean_text)

cat("\nSample cleaned tweets:\n")
for (i in 1:3) {
  cat(sprintf("  Original: %s\n", substr(df_sample$text[i], 1, 60)))
  cat(sprintf("  Cleaned:  %s\n", substr(df_sample$clean_text[i], 1, 60)))
  cat(sprintf("  Sentiment: %s\n\n", df_sample$sentiment[i]))
}

# ===== Step 3: Sentiment Analysis using Lexicon-Based Approach =====
# Using 'bing' lexicon (positive/negative words)
cat("Performing sentiment analysis using Bing lexicon...\n")

# Tokenize tweets into words
tweet_words <- df_sample %>%
  mutate(tweet_id = row_number()) %>%
  unnest_tokens(word, clean_text) %>%
  anti_join(stop_words, by = "word")  # Remove stop words

# Join with sentiment lexicon
bing_sentiments <- get_sentiments("bing")
tweet_sentiments <- tweet_words %>%
  inner_join(bing_sentiments, by = "word")

# Count positive and negative words per tweet
tweet_scores <- tweet_sentiments %>%
  group_by(tweet_id) %>%
  summarise(
    positive_words = sum(sentiment == "positive"),
    negative_words = sum(sentiment == "negative"),
    score = positive_words - negative_words
  )

# Assign predicted sentiment
tweet_scores$predicted_sentiment <- ifelse(
  tweet_scores$score > 0, "Positive",
  ifelse(tweet_scores$score < 0, "Negative", "Neutral")
)

# Merge back
df_sample$tweet_id <- 1:nrow(df_sample)
df_result <- merge(df_sample, tweet_scores[, c("tweet_id", "predicted_sentiment", "score")],
                   by = "tweet_id", all.x = TRUE)
df_result$predicted_sentiment[is.na(df_result$predicted_sentiment)] <- "Neutral"

# ===== Step 4: Sentiment Distribution =====
cat(sprintf("\n%s\n", strrep("=", 50)))
cat("  SENTIMENT ANALYSIS RESULTS\n")
cat(sprintf("%s\n", strrep("=", 50)))

sentiment_counts <- table(df_result$predicted_sentiment)
cat("\nSentiment Distribution:\n")
cat(sprintf("  %-12s %8s %12s\n", "Sentiment", "Count", "Percentage"))
cat(sprintf("  %-12s %8s %12s\n", strrep("-", 12), strrep("-", 8), strrep("-", 12)))
for (s in names(sentiment_counts)) {
  pct <- sentiment_counts[s] / nrow(df_result) * 100
  cat(sprintf("  %-12s %8d %10.1f%%\n", s, sentiment_counts[s], pct))
}

# ===== Step 5: Evaluate Accuracy =====
# Compare with actual labels (only for Positive/Negative)
eval_data <- df_result[df_result$predicted_sentiment != "Neutral", ]
eval_data$actual <- eval_data$sentiment
eval_data$predicted <- eval_data$predicted_sentiment

correct <- sum(eval_data$actual == eval_data$predicted)
total <- nrow(eval_data)
accuracy <- correct / total * 100

cat(sprintf("\n%s\n", strrep("=", 50)))
cat(sprintf("  MODEL ACCURACY: %.2f%%\n", accuracy))
cat(sprintf("%s\n", strrep("=", 50)))

# ===== Step 6: Most Common Sentiment Words =====
cat("\nTop 10 Positive Words:\n")
pos_words <- tweet_sentiments %>%
  filter(sentiment == "positive") %>%
  count(word, sort = TRUE) %>%
  head(10)
print(pos_words)

cat("\nTop 10 Negative Words:\n")
neg_words <- tweet_sentiments %>%
  filter(sentiment == "negative") %>%
  count(word, sort = TRUE) %>%
  head(10)
print(neg_words)

# ===== Step 7: Plot Bar Graph — Sentiment Distribution =====
sentiment_df <- as.data.frame(sentiment_counts)
colnames(sentiment_df) <- c("Sentiment", "Count")
sentiment_df$Percentage <- round(sentiment_df$Count / sum(sentiment_df$Count) * 100, 1)

ggplot(sentiment_df, aes(x = Sentiment, y = Count, fill = Sentiment)) +
  geom_bar(stat = "identity", color = "black", width = 0.6) +
  geom_text(aes(label = paste0(Count, "\n(", Percentage, "%)")),
            vjust = -0.5, fontface = "bold", size = 4) +
  scale_fill_manual(values = c("Negative" = "#e74c3c", 
                                "Neutral" = "#3498db", 
                                "Positive" = "#2ecc71")) +
  labs(title = "Sentiment Analysis - Tweet Distribution (Bar Chart)",
       x = "Sentiment", y = "Number of Tweets") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14),
        legend.position = "none") +
  ylim(0, max(sentiment_df$Count) * 1.15)

# ===== Step 8: Plot Pie Chart — Sentiment Distribution =====
ggplot(sentiment_df, aes(x = "", y = Count, fill = Sentiment)) +
  geom_bar(stat = "identity", width = 1, color = "white") +
  coord_polar("y", start = 0) +
  geom_text(aes(label = paste0(Sentiment, "\n", Percentage, "%")),
            position = position_stack(vjust = 0.5), size = 4) +
  scale_fill_manual(values = c("Negative" = "#e74c3c",
                                "Neutral" = "#3498db",
                                "Positive" = "#2ecc71")) +
  labs(title = "Sentiment Analysis - Distribution (Pie Chart)") +
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5, size = 14))

# ===== Step 9: Plot — Top Words by Sentiment =====
top_words <- tweet_sentiments %>%
  count(word, sentiment, sort = TRUE) %>%
  group_by(sentiment) %>%
  top_n(10, n) %>%
  ungroup()

ggplot(top_words, aes(x = reorder(word, n), y = n, fill = sentiment)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~sentiment, scales = "free_y") +
  coord_flip() +
  scale_fill_manual(values = c("negative" = "#e74c3c", "positive" = "#2ecc71")) +
  labs(title = "Top 10 Words by Sentiment",
       x = "Words", y = "Frequency") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14))