import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

TOTAL_FRAMES = 69175  # full first half length

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

active_time = []
for pid, records in by_id.items():
    frames_tracked = len(records)
    pct_active = (frames_tracked / TOTAL_FRAMES) * 100
    active_time.append({
        "id": pid,
        "frames_tracked": frames_tracked,
        "pct_active": round(pct_active, 2),
    })

with open("active_time.json", "w") as f:
    json.dump(active_time, f)

print(f"Players: {len(active_time)}")