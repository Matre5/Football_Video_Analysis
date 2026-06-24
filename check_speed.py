import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

by_id = defaultdict(list)

for d in data:
    by_id[d["id"]].append(d["speed_mps"])

for pid, speeds in by_id.items():
    print(
        pid,
        "max speed:",
        round(max(speeds),2),
        "avg:",
        round(sum(speeds)/len(speeds),2)
    )