import json
from collections import Counter

with open("tracks_filtered.json") as f:
    data=json.load(f)

counts = Counter(d["id"] for d in data)

for id_, frames in counts.most_common(20):
    print(id_, frames)