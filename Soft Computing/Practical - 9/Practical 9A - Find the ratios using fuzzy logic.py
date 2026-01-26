from fuzzywuzzy import fuzz
from fuzzywuzzy import process
s1="I love fuzzysforfuzzys"
s2="I am loving fuzzysforfuzzys"
print("FuzzyWuzzy Ratio:",fuzz.ratio(s1,s2))
print("FuzzyWuzzyPartialRatio:",fuzz.partial_ratio(s1,s2))
print("FuzzyWuzzyTokenSortRatio:",fuzz.token_sort_ratio(s1,s2))
print("FuzzyWuzzyTokenSetRatio:",fuzz.token_set_ratio(s1,s2))
print("FuzzyWuzzyWRatio:",fuzz.WRatio(s1,s2),'\n\n')
query='fuzzys for fuzzys'
choices=['fuzzys for fuzzys','fuzzy fuzzy','g. for fuzzys']
print("List of ratios:")
print(process.extract(query,choices),'\n')
print("Best among the above list: ",process.extractOne(query,choices))
