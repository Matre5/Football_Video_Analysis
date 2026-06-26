import json
from collections import defaultdict


FPS = 25
# Minimum observed frames needed before evaluating decline
# 250 frames = 10 seconds of tracking
MIN_TOTAL_SAMPLES = 250
# Percentage speed drop considered significant
FATIGUE_THRESHOLD = 20

with open("tracks_speed.json") as f:
    data = json.load(f)

players = defaultdict(list)
for d in data:
    players[d["id"]].append(d)


# Calculate intensity decline
results = []
for pid, records in players.items():
    records = sorted(records, key=lambda x: x["frame"])

    total_samples = len(records)

    # Too little observation
    if total_samples < MIN_TOTAL_SAMPLES:
        continue

    midpoint = total_samples // 2
    early = records[:midpoint]
    late = records[midpoint:]

    early_speed = sum(r["speed_mps"] for r in early) / len(early)
    late_speed = sum(r["speed_mps"] for r in late) / len(late)

    if early_speed > 0:
        decline = ((early_speed - late_speed) / early_speed) * 100
    else:
        decline = 0

    # Confidence
    duration_seconds = total_samples / FPS
    if total_samples >= 500:
        confidence = "high"
    elif total_samples >= 375:
        confidence = "medium"
    else:
        confidence = "limited"

    # Flag
    flag = decline >= FATIGUE_THRESHOLD

    results.append({
        "id": pid,
        "observed_duration_seconds": round(duration_seconds, 2),
        "early_avg_speed_mps": round(early_speed, 2),
        "late_avg_speed_mps": round(late_speed, 2),
        "speed_decline_percent": round(decline, 2),
        "observed_intensity_drop": flag,
        "confidence": confidence,
    })

with open("fatigue_results.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"Players evaluated: {len(results)}")
print(
    "Flagged for observed intensity decline:",
    sum(1 for r in results if r["observed_intensity_drop"]),
)