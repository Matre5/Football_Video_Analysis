import json
from collections import Counter

with open("tracks.json") as f:
    data = json.load(f)
    
id_counts = Counter(d["id"] for d in data)

MIN_FRAMES = 1000

# filtered = [d for d in data if id_counts[d["id"]] >= MIN_FRAMES]
filtered = [
    d for d in data
    if id_counts[d["id"]] >= MIN_FRAMES
    and d["h"] > 20
]

with open("tracks_filtered.json", "w") as f:
    json.dump(filtered, f)
    
print(f"Original data entries: {len(data)}")
print(f"Filtered data: {len(filtered)}")
print(f"Unique id: {len(id_counts)}")
print(f"Remaining unique id: {len(set(d['id'] for d in filtered))}")

