import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

SPRINT_THRESHOLD_MPS = 6.5
SPRINT_MIN_FRAMES = 8
MAX_HUMAN_SPEED = 12.4
DIP_TOLERANCE = 5   # allow up to 5 consecutive non-qualifying frames before ending the run

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

all_sprints = []

for pid, records in by_id.items():
    records.sort(key=lambda r: r["frame"])

    run_start_frame = None
    last_qualifying_frame = None
    dip_streak = 0

    for i, r in enumerate(records):
        qualifies = SPRINT_THRESHOLD_MPS <= r["speed_mps"] <= MAX_HUMAN_SPEED

        if qualifies:
            if run_start_frame is None:
                run_start_frame = records[i - 1]["frame"]
            last_qualifying_frame = r["frame"]
            dip_streak = 0
        else:
            if run_start_frame is not None:
                dip_streak += 1
                if dip_streak > DIP_TOLERANCE:
                    duration = last_qualifying_frame - run_start_frame
                    if duration >= SPRINT_MIN_FRAMES:
                        all_sprints.append({
                            "id": pid,
                            "start_frame": run_start_frame,
                            "end_frame": last_qualifying_frame,
                            "duration_frames": duration,
                        })
                    run_start_frame = None
                    dip_streak = 0

    if run_start_frame is not None:
        duration = last_qualifying_frame - run_start_frame
        if duration >= SPRINT_MIN_FRAMES:
            all_sprints.append({
                "id": pid,
                "start_frame": run_start_frame,
                "end_frame": last_qualifying_frame,
                "duration_frames": duration,
            })

with open("sprints.json", "w") as f:
    json.dump(all_sprints, f)

print(f"Total sprints detected: {len(all_sprints)}")