import json
import math
from collections import defaultdict

with open("tracks_scaled.json") as f:
    data = json.load(f)
    
FPS = 25
AVG_PL_height = 1.75

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

for pid, records in by_id.items():
    records.sort(key=lambda r: r["frame"])
    
    for i, r in enumerate(records):
        if i == 0:
            r['distance_m'] = 0.0
            r['speed_mps'] = 0.0
            r['gap_frames'] = 0
            continue
        
        prev = records[i - 1]

        avg_h = (r["smoothed_h"] + prev["smoothed_h"]) / 2
        meters_per_pixel = AVG_PL_height / avg_h

        pixel_dist = math.hypot(r["foot_x"] - prev["foot_x"], r["foot_y"] - prev["foot_y"])
        distance_m = pixel_dist * meters_per_pixel

        gap_frames = r["frame"] - prev["frame"]
        seconds = gap_frames / FPS
        speed_mps = distance_m / seconds if seconds > 0 else 0.0

        r["distance_m"] = distance_m
        r["speed_mps"] = speed_mps
        r["gap_frames"] = gap_frames

flattened = [r for records in by_id.values() for r in records]
with open("tracks_speed.json", "w") as f:
    json.dump(flattened, f)

print(f"Total records: {len(flattened)}")
            