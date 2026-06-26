import json
from collections import defaultdict

with open("tracks_stitched.json") as f:
    data = json.load(f)
    
ROLLING_WINDOW = 10

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)
    
for pid, records in by_id.items():
    records.sort(key=lambda r: r['frame'])
    
    for i, r in enumerate(records):
        foot_x = r['x']
        foot_y = r['y'] + r['h']/2
        
        r["foot_x"] = foot_x
        r["foot_y"] = foot_y
        
                
        window = records[max(0, i - ROLLING_WINDOW + 1): i + 1]
        r["smoothed_h"] = sum(rec["h"] for rec in window) / len(window)

flattened = [r for records in by_id.values() for r in records]

with open("tracks_scaled.json", "w") as f:
    json.dump(flattened, f)

print(f"Total records: {len(flattened)}")
        