import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

GRID_COLS, GRID_ROWS = 6, 4

all_x = [d["foot_x"] for d in data]
all_y = [d["foot_y"] for d in data]
min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

heatmaps = {}
for pid, records in by_id.items():
    grid = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
    for r in records:
        col = min(int((r["foot_x"] - min_x) / (max_x - min_x) * GRID_COLS), GRID_COLS - 1)
        row = min(int((r["foot_y"] - min_y) / (max_y - min_y) * GRID_ROWS), GRID_ROWS - 1)
        grid[row][col] += 1
    heatmaps[pid] = grid

with open("heatmaps.json", "w") as f:
    json.dump(heatmaps, f)

print(f"Heatmaps built for {len(heatmaps)} players")