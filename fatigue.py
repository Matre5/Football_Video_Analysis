import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

MIN_TOTAL_SAMPLES = 60   # need enough data to say anything meaningful
DECLINE_THRESHOLD_PCT = -20   # flag if speed drops more than a fifth vs their own earlier baseline

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

fatigue_results = []

for pid, records in by_id.items():
    records.sort(key=lambda r: r["frame"])
    if len(records) < MIN_TOTAL_SAMPLES:
        continue

    mid = len(records) // 2
    first_half = records[:mid]
    second_half = records[mid:]

    avg_first = sum(r["speed_mps"] for r in first_half) / len(first_half)
    avg_second = sum(r["speed_mps"] for r in second_half) / len(second_half)

    pct_change = ((avg_second - avg_first) / avg_first) * 100 if avg_first > 0 else 0

    fatigue_results.append({
        "id": pid,
        "samples": len(records),
        "avg_speed_early": round(avg_first, 2),
        "avg_speed_late": round(avg_second, 2),
        "pct_change": round(pct_change, 1),
        "fatigue_flag": pct_change <= DECLINE_THRESHOLD_PCT,
    })

with open("fatigue.json", "w") as f:
    json.dump(fatigue_results, f)

print(f"Players evaluated: {len(fatigue_results)}")
print(f"Flagged for elevated fatigue: {sum(1 for r in fatigue_results if r['fatigue_flag'])}")