# Required libraries
library(reshape2)   # Pivot/melt
library(ggplot2)    # Heatmap plotting
library(proxy)      # Cosine similarity

# ===== Step 1: Load the MovieLens 100K Dataset =====
url_ratings <- "https://raw.githubusercontent.com/sparsh-ai/rec-data-public/master/ml-100k/u.data"
url_movies <- "https://raw.githubusercontent.com/sparsh-ai/rec-data-public/master/ml-100k/u.item"

ratings <- read.delim(url_ratings, header = FALSE, sep = "\t",
                      col.names = c("user_id", "movie_id", "rating", "timestamp"))

movies <- read.delim(url_movies, header = FALSE, sep = "|", 
                     quote = "", encoding = "latin1")[, 1:2]
colnames(movies) <- c("movie_id", "title")

# --- If files are downloaded locally, use this instead: ---
# ratings <- read.delim("u.data", header=FALSE, sep="\t",
#                       col.names=c("user_id","movie_id","rating","timestamp"))
# movies <- read.delim("u.item", header=FALSE, sep="|", quote="", encoding="latin1")[,1:2]
# colnames(movies) <- c("movie_id", "title")
# -----------------------------------------------------------

cat("Ratings shape:", nrow(ratings), "x", ncol(ratings), "\n")
cat("Movies:", nrow(movies), "\n")
cat("\nFirst 5 ratings:\n")
print(head(ratings, 5))
cat(sprintf("\nTotal Users: %d\n", length(unique(ratings$user_id))))
cat(sprintf("Total Movies: %d\n", length(unique(ratings$movie_id))))
cat(sprintf("Total Ratings: %d\n", nrow(ratings)))

# ===== Step 2: Create User-Item Matrix =====
user_item_matrix <- dcast(ratings, user_id ~ movie_id, value.var = "rating")
rownames(user_item_matrix) <- user_item_matrix$user_id
user_item_matrix$user_id <- NULL

cat(sprintf("\nUser-Item Matrix: %d users x %d movies\n", 
            nrow(user_item_matrix), ncol(user_item_matrix)))

# Fill NA with 0 for similarity computation
ui_filled <- user_item_matrix
ui_filled[is.na(ui_filled)] <- 0

# ===== Step 3: Compute User-User Cosine Similarity =====
user_sim <- as.matrix(simil(as.matrix(ui_filled), method = "cosine"))
cat("User-User Similarity Matrix computed:", dim(user_sim), "\n")

# ===== Step 4: Compute Item-Item Similarity =====
item_sim <- as.matrix(simil(as.matrix(t(ui_filled)), method = "cosine"))
cat("Item-Item Similarity Matrix computed:", dim(item_sim), "\n")

# ===== Step 5: Predict Ratings (User-Based CF) =====
predict_rating <- function(user_id, movie_id, k = 10) {
  user_idx <- which(rownames(user_item_matrix) == user_id)
  movie_col <- as.character(movie_id)
  
  if (!(movie_col %in% colnames(user_item_matrix))) return(3.0)
  
  # Get movie ratings from all users
  movie_ratings <- user_item_matrix[, movie_col]
  
  # Users who rated this movie
  rated_idx <- which(!is.na(movie_ratings))
  
  if (length(rated_idx) == 0) return(3.0)
  
  # Get similarities with those users
  sims <- user_sim[user_idx, rated_idx]
  
  # Top K similar users
  top_k_idx <- order(sims, decreasing = TRUE)[1:min(k, length(sims))]
  top_k_sims <- sims[top_k_idx]
  top_k_ratings <- movie_ratings[rated_idx[top_k_idx]]
  
  if (sum(top_k_sims, na.rm = TRUE) == 0) return(mean(movie_ratings, na.rm = TRUE))
  
  # Weighted average
  pred <- sum(top_k_sims * top_k_ratings, na.rm = TRUE) / sum(top_k_sims, na.rm = TRUE)
  return(round(pred, 2))
}

# ===== Step 6: Generate Recommendations =====
get_recommendations <- function(user_id, n = 10) {
  user_idx <- which(rownames(user_item_matrix) == user_id)
  user_ratings <- user_item_matrix[user_idx, ]
  
  # Unrated movies
  unrated <- which(is.na(user_ratings))
  
  # Predict for unrated (limit for speed)
  predictions <- data.frame(movie_id = integer(), pred_rating = numeric())
  
  for (i in unrated[1:min(200, length(unrated))]) {
    movie_id <- as.integer(colnames(user_item_matrix)[i])
    pred <- predict_rating(user_id, movie_id)
    predictions <- rbind(predictions, data.frame(movie_id = movie_id, pred_rating = pred))
  }
  
  # Sort and get top N
  predictions <- predictions[order(-predictions$pred_rating), ]
  top_n <- head(predictions, n)
  
  # Add movie titles
  top_n <- merge(top_n, movies, by = "movie_id")
  return(top_n[order(-top_n$pred_rating), c("title", "pred_rating")])
}

# Get recommendations for User 1
cat(sprintf("\n%s\n", strrep("=", 60)))
cat("  TOP 10 RECOMMENDATIONS FOR USER 1\n")
cat(sprintf("%s\n", strrep("=", 60)))

recs <- get_recommendations(user_id = 1, n = 10)
cat(sprintf("\n  %-40s %12s\n", "MOVIE TITLE", "PRED RATING"))
cat(sprintf("  %-40s %12s\n", strrep("-", 40), strrep("-", 12)))
for (i in seq_len(nrow(recs))) {
  cat(sprintf("  %-40s %10.2f\n", substr(recs$title[i], 1, 40), recs$pred_rating[i]))
}

# ===== Step 7: Evaluate Model =====
cat(sprintf("\n%s\n", strrep("=", 60)))
cat("  MODEL EVALUATION\n")
cat(sprintf("%s\n", strrep("=", 60)))

set.seed(42)
test_idx <- sample(1:nrow(ratings), 500)
test_set <- ratings[test_idx, ]

actual <- numeric()
predicted <- numeric()

for (i in 1:nrow(test_set)) {
  pred <- predict_rating(test_set$user_id[i], test_set$movie_id[i])
  actual <- c(actual, test_set$rating[i])
  predicted <- c(predicted, pred)
}

rmse <- sqrt(mean((actual - predicted)^2, na.rm = TRUE))
mae <- mean(abs(actual - predicted), na.rm = TRUE)
cat(sprintf("\n  RMSE: %.4f\n", rmse))
cat(sprintf("  MAE:  %.4f\n", mae))

# ===== Step 8: Plot Heatmap — User-User Similarity =====
# Top 20 users
subset_sim <- user_sim[1:20, 1:20]
melted_sim <- melt(subset_sim)
colnames(melted_sim) <- c("User1", "User2", "Similarity")

ggplot(melted_sim, aes(x = User1, y = User2, fill = Similarity)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "red") +
  labs(title = "User-User Similarity Heatmap (Top 20 Users)",
       x = "User ID", y = "User ID") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14))

# ===== Step 9: Plot Heatmap — Item-Item Similarity =====
# Top 20 most-rated movies
top_20_movies <- names(sort(colSums(!is.na(user_item_matrix)), decreasing = TRUE))[1:20]
top_20_idx <- which(colnames(ui_filled) %in% top_20_movies)
subset_item_sim <- item_sim[top_20_idx, top_20_idx]

# Get movie titles for labels
movie_labels <- sapply(top_20_movies, function(m) {
  title <- movies$title[movies$movie_id == as.integer(m)]
  substr(title[1], 1, 20)
})

rownames(subset_item_sim) <- movie_labels
colnames(subset_item_sim) <- movie_labels
melted_item <- melt(subset_item_sim)
colnames(melted_item) <- c("Movie1", "Movie2", "Similarity")

ggplot(melted_item, aes(x = Movie1, y = Movie2, fill = Similarity)) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0.5) +
  labs(title = "Item-Item Similarity Heatmap (Top 20 Movies)",
       x = "", y = "") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7),
        axis.text.y = element_text(size = 7),
        plot.title = element_text(hjust = 0.5, size = 13))

# ===== Step 10: Plot Heatmap — User-Item Rating Matrix =====
top_15_users <- rownames(user_item_matrix)[1:15]
top_15_movies <- names(sort(colSums(!is.na(user_item_matrix)), decreasing = TRUE))[1:15]
subset_ui <- user_item_matrix[top_15_users, top_15_movies]

movie_labels_15 <- sapply(top_15_movies, function(m) {
  substr(movies$title[movies$movie_id == as.integer(m)][1], 1, 18)
})
colnames(subset_ui) <- movie_labels_15

melted_ui <- melt(as.matrix(subset_ui))
colnames(melted_ui) <- c("User", "Movie", "Rating")

ggplot(melted_ui, aes(x = Movie, y = User, fill = Rating)) +
  geom_tile(color = "grey90") +
  scale_fill_viridis_c(na.value = "white", name = "Rating") +
  labs(title = "User-Item Rating Matrix (15 Users × 15 Movies)",
       x = "Movies", y = "User ID") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 8),
        plot.title = element_text(hjust = 0.5, size = 13))