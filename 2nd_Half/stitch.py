import json
from collections import defaultdict
import math

with open("tracks_filtered.json") as f:
    data = json.load(f)

# 3 seconds at 25fps — a reasoned middle value for typical broadcast
MAX_GAP_FRAMES = 75

HEIGHT_MULTIPLIER = 6

# collapse every detection down into one summary per id
segments = defaultdict(lambda: {"first_frame": None, "last_frame": None})
for d in data:
    seg = segments[d["id"]]
    if seg["first_frame"] is None or d["frame"] < seg["first_frame"]:
        seg["first_frame"] = d["frame"]
        seg["first_x"], seg["first_y"] = d["x"], d["y"]
    if seg["last_frame"] is None or d["frame"] > seg["last_frame"]:
        seg["last_frame"] = d["frame"]
        seg["last_x"], seg["last_y"] = d["x"], d["y"]
        seg["last_h"] = d["h"]   # height at the moment it disappeared

segment_list = [{"id": id_, **seg} for id_, seg in segments.items()]
segment_list.sort(key=lambda s: s["first_frame"])

merge_map = {}        # old_id -> new_id
available = []        # candidate segments not yet claimed by a later match

for seg in segment_list:
    best_match = None
    best_dist = None

    for cand in available:
        gap = seg["first_frame"] - cand["last_frame"]
        if gap <= 0 or gap > MAX_GAP_FRAMES:
            continue

        dist = math.hypot(seg["first_x"] - cand["last_x"], seg["first_y"] - cand["last_y"])
        seconds = gap / 25.0
        max_allowed = HEIGHT_MULTIPLIER * cand["last_h"] * seconds

        if dist <= max_allowed:
            if best_dist is None or dist < best_dist:
                best_match = cand
                best_dist = dist

    if best_match is not None:
        merge_map[seg["id"]] = best_match["id"]
        available.remove(best_match)
        # the merged segment can itself be continued later, so it stays
        # "available" under its own root id, carrying this segment's end state
        best_match["last_frame"] = seg["last_frame"]
        best_match["last_x"] = seg["last_x"]
        best_match["last_y"] = seg["last_y"]
        best_match["last_h"] = seg["last_h"]
        available.append(best_match)
    else:
        available.append(seg)

# apply the merges to the full dataset
for d in data:
    while d["id"] in merge_map:
        d["id"] = merge_map[d["id"]]

with open("tracks_stitched.json", "w") as f:
    json.dump(data, f)

print(f"Before stitching: {len(segment_list)} segments")
print(f"After stitching: {len(set(d['id'] for d in data))} unique players")