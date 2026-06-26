# Required libraries
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# ===== Step 1: Load the MovieLens 100K Dataset =====
url_ratings = "https://raw.githubusercontent.com/sparsh-ai/rec-data-public/master/ml-100k/u.data"
url_movies = "https://raw.githubusercontent.com/sparsh-ai/rec-data-public/master/ml-100k/u.item"

# Load ratings (tab-separated: user_id, movie_id, rating, timestamp)
ratings = pd.read_csv(url_ratings, sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])

# Load movie titles (pipe-separated)
movies = pd.read_csv(url_movies, sep='|', encoding='latin-1', header=None,
                     usecols=[0, 1], names=['movie_id', 'title'])

# --- If files are downloaded locally, use this instead: ---
# ratings = pd.read_csv("u.data", sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
# movies = pd.read_csv("u.item", sep='|', encoding='latin-1', header=None,
#                      usecols=[0, 1], names=['movie_id', 'title'])
# -----------------------------------------------------------

print("Ratings shape:", ratings.shape)
print("Movies shape:", movies.shape)
print("\nRatings sample:")
print(ratings.head())
print(f"\nTotal Users: {ratings['user_id'].nunique()}")
print(f"Total Movies: {ratings['movie_id'].nunique()}")
print(f"Total Ratings: {len(ratings)}")
print(f"Rating range: {ratings['rating'].min()} to {ratings['rating'].max()}")

# ===== Step 2: Create User-Item Matrix =====
user_item_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating')
print(f"\nUser-Item Matrix shape: {user_item_matrix.shape}")
print(f"Sparsity: {1 - (ratings.shape[0] / (user_item_matrix.shape[0] * user_item_matrix.shape[1])):.4f}")

# Fill NaN with 0 for similarity computation
user_item_filled = user_item_matrix.fillna(0)

# ===== Step 3: Compute User-User Similarity (Cosine Similarity) =====
user_similarity = cosine_similarity(user_item_filled)
user_similarity_df = pd.DataFrame(user_similarity, 
                                   index=user_item_matrix.index,
                                   columns=user_item_matrix.index)
print("\nUser-User Similarity Matrix shape:", user_similarity_df.shape)
print("\nSample similarities (User 1 vs others):")
print(user_similarity_df.iloc[0, 1:6])

# ===== Step 4: Compute Item-Item Similarity =====
item_similarity = cosine_similarity(user_item_filled.T)
item_similarity_df = pd.DataFrame(item_similarity,
                                   index=user_item_matrix.columns,
                                   columns=user_item_matrix.columns)
print("\nItem-Item Similarity Matrix shape:", item_similarity_df.shape)

# ===== Step 5: Predict Ratings (User-Based Collaborative Filtering) =====
def predict_user_based(user_id, movie_id, k=10):
    """Predict rating for a user-movie pair using K nearest neighbors"""
    # Check if user has rated this movie
    if movie_id not in user_item_matrix.columns:
        return 3.0  # Default rating
    
    # Get similarity scores for this user with all others
    sim_scores = user_similarity_df[user_id]
    
    # Get ratings for this movie by all users
    movie_ratings = user_item_matrix[movie_id]
    
    # Find users who rated this movie
    rated_users = movie_ratings.dropna().index
    
    # Get top-K similar users who rated this movie
    similar_users = sim_scores[rated_users].sort_values(ascending=False)[1:k+1]
    
    if similar_users.empty or similar_users.sum() == 0:
        return movie_ratings.mean()
    
    # Weighted average: sum(similarity * rating) / sum(similarity)
    weighted_sum = sum(similar_users[u] * movie_ratings[u] for u in similar_users.index)
    prediction = weighted_sum / similar_users.sum()
    
    return round(prediction, 2)

# ===== Step 6: Generate Recommendations =====
def get_recommendations(user_id, n=10):
    """Get top-N movie recommendations for a user"""
    # Movies already rated by user
    rated_movies = user_item_matrix.loc[user_id].dropna().index.tolist()
    
    # Movies not yet rated
    unrated_movies = [m for m in user_item_matrix.columns if m not in rated_movies]
    
    # Predict ratings for unrated movies
    predictions = []
    for movie_id in unrated_movies[:200]:  # Limit for speed
        pred = predict_user_based(user_id, movie_id)
        predictions.append((movie_id, pred))
    
    # Sort by predicted rating
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    # Get top N
    top_n = predictions[:n]
    
    # Map to movie titles
    recommendations = []
    for movie_id, pred_rating in top_n:
        title = movies[movies['movie_id'] == movie_id]['title'].values
        title = title[0] if len(title) > 0 else f"Movie {movie_id}"
        recommendations.append((title, pred_rating))
    
    return recommendations

# Get recommendations for User 1
print("\n" + "="*60)
print("  TOP 10 RECOMMENDATIONS FOR USER 1")
print("="*60)
recs = get_recommendations(user_id=1, n=10)
print(f"\n  {'MOVIE TITLE':<45} {'PREDICTED RATING':>16}")
print(f"  {'-'*45} {'-'*16}")
for title, rating in recs:
    print(f"  {title:<45} {rating:>10.2f}")

# ===== Step 7: Evaluate Model (Train-Test Split) =====
print("\n" + "="*60)
print("  MODEL EVALUATION")
print("="*60)

train, test = train_test_split(ratings, test_size=0.2, random_state=42)
print(f"\n  Training set: {len(train)} ratings")
print(f"  Test set: {len(test)} ratings")

# Build matrix from training data
train_matrix = train.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)
train_similarity = cosine_similarity(train_matrix)
train_sim_df = pd.DataFrame(train_similarity, index=train_matrix.index, columns=train_matrix.index)

# Predict on test set (sample for speed)
test_sample = test.sample(n=500, random_state=42)
actual = []
predicted = []

for _, row in test_sample.iterrows():
    user = row['user_id']
    movie = row['movie_id']
    if user in train_matrix.index and movie in train_matrix.columns:
        pred = predict_user_based(user, movie, k=10)
        actual.append(row['rating'])
        predicted.append(pred)

rmse = np.sqrt(mean_squared_error(actual, predicted))
mae = np.mean(np.abs(np.array(actual) - np.array(predicted)))
print(f"\n  RMSE: {rmse:.4f}")
print(f"  MAE:  {mae:.4f}")

# ===== Step 8: Plot Heatmap — User-User Similarity =====
plt.figure(figsize=(10, 8))
# Plot top 20 users for readability
subset_sim = user_similarity_df.iloc[:20, :20]
sns.heatmap(subset_sim, annot=False, cmap='YlOrRd', 
            xticklabels=True, yticklabels=True,
            linewidths=0.5, vmin=0, vmax=1)
plt.title("User-User Similarity Heatmap (Top 20 Users)", fontsize=14)
plt.xlabel("User ID")
plt.ylabel("User ID")
plt.tight_layout()
plt.savefig("user_similarity_heatmap.png")
plt.show()

# ===== Step 9: Plot Heatmap — Item-Item Similarity =====
plt.figure(figsize=(10, 8))
# Select top 20 most-rated movies
top_movies = ratings['movie_id'].value_counts().head(20).index.tolist()
subset_item_sim = item_similarity_df.loc[top_movies, top_movies]

# Get movie titles for labels
movie_labels = [movies[movies['movie_id'] == m]['title'].values[0][:20] for m in top_movies]

sns.heatmap(subset_item_sim, annot=True, fmt='.2f', cmap='coolwarm',
            xticklabels=movie_labels, yticklabels=movie_labels,
            linewidths=0.5, vmin=0, vmax=1)
plt.title("Item-Item Similarity Heatmap (Top 20 Movies)", fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig("item_similarity_heatmap.png")
plt.show()

# ===== Step 10: Plot Heatmap — User-Item Rating Matrix =====
plt.figure(figsize=(12, 8))
# Top 30 users x Top 30 movies
top_users = ratings['user_id'].value_counts().head(30).index.tolist()
top_movies_30 = ratings['movie_id'].value_counts().head(30).index.tolist()
subset_matrix = user_item_matrix.loc[top_users, top_movies_30]

movie_labels_30 = [movies[movies['movie_id'] == m]['title'].values[0][:15] for m in top_movies_30]

sns.heatmap(subset_matrix, cmap='viridis', xticklabels=movie_labels_30,
            yticklabels=True, linewidths=0.1, cbar_kws={'label': 'Rating'})
plt.title("User-Item Rating Matrix Heatmap (Top 30 Users × Top 30 Movies)", fontsize=13)
plt.xlabel("Movies")
plt.ylabel("User ID")
plt.xticks(rotation=45, ha='right', fontsize=7)
plt.tight_layout()
plt.savefig("user_item_heatmap.png")
plt.show()