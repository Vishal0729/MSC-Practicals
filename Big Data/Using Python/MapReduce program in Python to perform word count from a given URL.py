from functools import reduce
import urllib.request
import re
from collections import defaultdict

url = "https://www.gutenberg.org/files/1342/1342-0.txt"
response = urllib.request.urlopen(url)
text = response.read().decode('utf-8')

lines = text.split('\n')
print(f"Total lines downloaded: {len(lines)}")

def mapper(line):
    words = re.findall(r'[a-z]+', line.lower())
    return [(word, 1) for word in words]


def shuffle_and_sort(mapped_data):
    shuffled = defaultdict(list)
    for key, value in mapped_data:
        shuffled[key].append(value)
    return shuffled


def reducer(word, counts):
    return (word, sum(counts))


print("\n" + "="*60)
print("         MAPREDUCE WORD COUNT")
print("="*60)

print("\n[Step 1] MAP Phase - Processing lines...")
mapped_results = []
for line in lines:
    mapped_results.extend(mapper(line))
print(f"  Total (word, 1) pairs emitted: {len(mapped_results)}")

print("\n[Step 2] SHUFFLE & SORT Phase - Grouping by key...")
shuffled_data = shuffle_and_sort(mapped_results)
print(f"  Unique words found: {len(shuffled_data)}")

print("\n[Step 3] REDUCE Phase - Aggregating counts...")
reduced_results = []
for word, counts in shuffled_data.items():
    reduced_results.append(reducer(word, counts))

reduced_results.sort(key=lambda x: x[1], reverse=True)

print("\n" + "-"*40)
print("  TOP 25 MOST FREQUENT WORDS")
print("-"*40)
print(f"  {'WORD':<20} {'COUNT':>10}")
print(f"  {'----':<20} {'-----':>10}")
for word, count in reduced_results[:25]:
    print(f"  {word:<20} {count:>10}")

print(f"\n  Total unique words: {len(reduced_results)}")
print(f"  Total word occurrences: {sum(c for _, c in reduced_results)}")