import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

SPRINT_THRESHOLD_MPS = 7
SPRINT_MIN_FRAMES = 25
MAX_HUMAN_SPEED = 12.4

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

all_sprints = []

for pid, records in by_id.items():
    records.sort(key=lambda r: r["frame"])

    run_start_frame = None

    for i, r in enumerate(records):
        qualifies = SPRINT_THRESHOLD_MPS <= r["speed_mps"] <= MAX_HUMAN_SPEED

        if qualifies:
            if run_start_frame is None:
                run_start_frame = records[i - 1]["frame"]
        else:
            if run_start_frame is not None:
                duration = r["frame"] - run_start_frame
                if duration >= SPRINT_MIN_FRAMES:
                    all_sprints.append({
                        "id": pid,
                        "start_frame": run_start_frame,
                        "end_frame": r["frame"],
                        "duration_frames": duration,
                    })
            run_start_frame = None

    if run_start_frame is not None:
        last_frame = records[-1]["frame"]
        duration = last_frame - run_start_frame
        if duration >= SPRINT_MIN_FRAMES:
            all_sprints.append({
                "id": pid,
                "start_frame": run_start_frame,
                "end_frame": last_frame,
                "duration_frames": duration,
            })

with open("sprints.json", "w") as f:
    json.dump(all_sprints, f)

print(f"Total sprints detected: {len(all_sprints)}")