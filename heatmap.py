import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

GRID_COLS = 12
GRID_ROWS = 8

# video dimensions
WIDTH = 398
HEIGHT = 224


by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

heatmaps = {}
for pid, records in by_id.items():

    grid = [
        [0 for _ in range(GRID_COLS)]
        for _ in range(GRID_ROWS)
    ]
    for r in records:

        x = r["foot_x"]
        y = r["foot_y"]
        
        # ---- Perspective correction
        # Bottom of image represents near side
        # Top of image represents far side
        #

        pitch_x = x / WIDTH

        # remove camera horizon
        pitch_y = (y - 80) / (HEIGHT - 80)

        # clamp
        pitch_x = max(0, min(1, pitch_x))
        pitch_y = max(0, min(1, pitch_y))

        col = int(pitch_x * GRID_COLS)
        row = int(pitch_y * GRID_ROWS)

        col = min(col, GRID_COLS-1)
        row = min(row, GRID_ROWS-1)

        grid[row][col] += 1

    heatmaps[str(pid)] = grid

with open("heatmaps.json", "w") as f:
    json.dump(heatmaps, f)

print(f"Heatmaps built for {len(heatmaps)} players")