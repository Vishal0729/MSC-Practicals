# Required libraries
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from collections import Counter
import matplotlib.pyplot as plt

# ===== Step 1: Load the Sentiment140 Dataset =====
url = "https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv"
df = pd.read_csv(url, encoding='latin-1', header=None,
                 names=['target', 'id', 'date', 'flag', 'user', 'text'])

# --- If file is downloaded locally (from Kaggle), use this instead: ---
# df = pd.read_csv("training.1600000.processed.noemoticon.csv", 
#                  encoding='latin-1', header=None,
#                  names=['target', 'id', 'date', 'flag', 'user', 'text'])
# ----------------------------------------------------------------------

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df[['target', 'text']].head())
print("\nTarget distribution (0=Negative, 4=Positive):")
print(df['target'].value_counts())

# ===== Step 2: Data Preprocessing =====
# Map labels: 0=Negative, 2=Neutral, 4=Positive -> 0, 1, 2
df['sentiment'] = df['target'].map({0: 'Negative', 2: 'Neutral', 4: 'Positive'})

# Take sample for faster processing (full dataset is 1.6M)
df_sample = df.sample(n=50000, random_state=42).reset_index(drop=True)
print(f"\nWorking with sample: {len(df_sample)} tweets")

# Text cleaning function
def clean_text(text):
    """Remove URLs, mentions, hashtags, special characters"""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)       # Remove URLs
    text = re.sub(r'@\w+', '', text)                  # Remove @mentions
    text = re.sub(r'#\w+', '', text)                  # Remove hashtags
    text = re.sub(r'rt\s+', '', text)                 # Remove RT
    text = re.sub(r'[^a-zA-Z\s]', '', text)           # Remove special chars
    text = re.sub(r'\s+', ' ', text).strip()          # Remove extra spaces
    return text

print("\nCleaning text data...")
df_sample['clean_text'] = df_sample['text'].apply(clean_text)

print("\nSample cleaned tweets:")
for i in range(3):
    print(f"  Original: {df_sample['text'].iloc[i][:60]}...")
    print(f"  Cleaned:  {df_sample['clean_text'].iloc[i][:60]}...")
    print(f"  Sentiment: {df_sample['sentiment'].iloc[i]}\n")

# ===== Step 3: Feature Extraction using TF-IDF =====
tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), stop_words='english')
X = tfidf.fit_transform(df_sample['clean_text'])
y = df_sample['target'].map({0: 0, 4: 1})  # Binary: 0=Negative, 1=Positive

print(f"TF-IDF Matrix shape: {X.shape}")

# ===== Step 4: Train-Test Split =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTraining samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

# ===== Step 5: Build Sentiment Classification Model =====
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
print("\nLogistic Regression model trained!")

# ===== Step 6: Evaluate Model =====
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*50}")
print(f"  MODEL ACCURACY: {accuracy * 100:.2f}%")
print(f"{'='*50}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))

# ===== Step 7: Analyze Sentiments on Full Sample =====
print("\n" + "="*50)
print("  SENTIMENT ANALYSIS RESULTS")
print("="*50)

# Predict sentiments for all tweets
all_predictions = model.predict(X)
df_sample['predicted_sentiment'] = ['Positive' if p == 1 else 'Negative' for p in all_predictions]

# Add neutral category based on prediction probability
probs = model.predict_proba(X)
df_sample['predicted_sentiment'] = np.where(
    (probs[:, 1] > 0.4) & (probs[:, 1] < 0.6), 'Neutral',
    np.where(probs[:, 1] >= 0.6, 'Positive', 'Negative')
)

# Count sentiments
sentiment_counts = df_sample['predicted_sentiment'].value_counts()
print("\nSentiment Distribution:")
print(f"  {'Sentiment':<12} {'Count':>8} {'Percentage':>12}")
print(f"  {'-'*12} {'-'*8} {'-'*12}")
for sentiment, count in sentiment_counts.items():
    pct = count / len(df_sample) * 100
    print(f"  {sentiment:<12} {count:>8} {pct:>10.1f}%")

# ===== Step 8: Test with Custom Tweets =====
print("\n" + "="*50)
print("  PREDICT CUSTOM TWEETS")
print("="*50)

custom_tweets = [
    "I love this product! Best purchase ever!",
    "Terrible service, never going back again",
    "The weather is okay today, nothing special",
    "Absolutely amazing experience, highly recommend!",
    "I hate waiting in long queues, so frustrating",
    "Just had lunch, it was alright"
]

custom_clean = [clean_text(t) for t in custom_tweets]
custom_tfidf = tfidf.transform(custom_clean)
custom_preds = model.predict(custom_tfidf)
custom_probs = model.predict_proba(custom_tfidf)

print(f"\n  {'TWEET':<50} {'SENTIMENT':<10} {'CONFIDENCE':>10}")
print(f"  {'-'*50} {'-'*10} {'-'*10}")
for tweet, pred, prob in zip(custom_tweets, custom_preds, custom_probs):
    sentiment = 'Positive' if pred == 1 else 'Negative'
    confidence = max(prob) * 100
    print(f"  {tweet[:50]:<50} {sentiment:<10} {confidence:>8.1f}%")

# ===== Step 9: Plot Bar Graph — Sentiment Distribution =====
plt.figure(figsize=(8, 6))
colors = {'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#3498db'}
bars = plt.bar(sentiment_counts.index, sentiment_counts.values,
               color=[colors.get(s, 'gray') for s in sentiment_counts.index],
               edgecolor='black', linewidth=1.2)

# Add value labels on bars
for bar, count in zip(bars, sentiment_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f'{count}\n({count/len(df_sample)*100:.1f}%)',
             ha='center', fontsize=11, fontweight='bold')

plt.xlabel("Sentiment", fontsize=12)
plt.ylabel("Number of Tweets", fontsize=12)
plt.title("Sentiment Analysis - Tweet Distribution", fontsize=14)
plt.tight_layout()
plt.savefig("sentiment_bar_chart.png")
plt.show()

# ===== Step 10: Plot Pie Chart — Sentiment Distribution =====
plt.figure(figsize=(8, 8))
colors_list = [colors.get(s, 'gray') for s in sentiment_counts.index]
explode = [0.05] * len(sentiment_counts)

plt.pie(sentiment_counts.values, labels=sentiment_counts.index,
        autopct='%1.1f%%', startangle=140, colors=colors_list,
        explode=explode, shadow=True, textprops={'fontsize': 12})
plt.title("Sentiment Analysis - Distribution (Pie Chart)", fontsize=14)
plt.tight_layout()
plt.savefig("sentiment_pie_chart.png")
plt.show()

# ===== Step 11: Plot — Most Common Words per Sentiment =====
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for idx, sentiment in enumerate(['Positive', 'Negative']):
    subset = df_sample[df_sample['predicted_sentiment'] == sentiment]['clean_text']
    all_words = ' '.join(subset).split()
    common_words = Counter(all_words).most_common(10)
    words, counts = zip(*common_words)
    
    axes[idx].barh(words, counts, color=colors[sentiment], edgecolor='black')
    axes[idx].set_title(f"Top 10 Words - {sentiment}", fontsize=12)
    axes[idx].set_xlabel("Frequency")
    axes[idx].invert_yaxis()

plt.suptitle("Most Common Words by Sentiment", fontsize=14)
plt.tight_layout()
plt.savefig("sentiment_common_words.png")
plt.show()