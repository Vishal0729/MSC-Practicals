from collections import defaultdict
import re

text_data = [
    "Hello world",
    "Hello from the other side",
    "world of MapReduce",
    "MapReduce is powerful"
]

print("="*60)
print("     MAPREDUCE WORD COUNT - CUSTOM TEXT DATASET")
print("="*60)
print("\nInput Data:")
for i, line in enumerate(text_data):
    print(f"  Line {i+1}: \"{line}\"")


def mapper(line):
    words = re.findall(r'[a-z]+', line.lower())
    pairs = [(word, 1) for word in words]
    return pairs


def shuffle_and_sort(mapped_data):
    shuffled = defaultdict(list)
    for key, value in mapped_data:
        shuffled[key].append(value)
    return dict(sorted(shuffled.items()))


def reducer(word, counts):
    return (word, sum(counts))


print("\n" + "-"*60)
print("[Step 1] MAP Phase")
print("-"*60)

all_mapped = []
for line in text_data:
    mapped = mapper(line)
    print(f"  \"{line}\"")
    print(f"    -> {mapped}")
    all_mapped.extend(mapped)

print(f"\n  Combined mapped output ({len(all_mapped)} pairs):")
print(f"  {all_mapped}")

print("\n" + "-"*60)
print("[Step 2] SHUFFLE & SORT Phase")
print("-"*60)

shuffled = shuffle_and_sort(all_mapped)
for word, counts in shuffled.items():
    print(f"  {word:<15} -> {counts}")

print("\n" + "-"*60)
print("[Step 3] REDUCE Phase")
print("-"*60)

final_results = []
for word, counts in shuffled.items():
    result = reducer(word, counts)
    final_results.append(result)
    print(f"  {word:<15}: sum({counts}) = {result[1]}")

print("\n" + "="*60)
print("  FINAL WORD COUNT RESULTS")
print("="*60)
print(f"  {'WORD':<15} {'COUNT':>5}")
print(f"  {'-'*15} {'-'*5}")

final_results.sort(key=lambda x: x[1], reverse=True)
for word, count in final_results:
    print(f"  {word:<15} {count:>5}")

print(f"\n  Total unique words: {len(final_results)}")
print(f"  Total word count: {sum(c for _, c in final_results)}")