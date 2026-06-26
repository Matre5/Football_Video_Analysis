import json
import cv2
import numpy as np
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

# Your video pitch corners
src_points = np.float32([
    [53, 86],
    [362, 84],
    [394, 236],
    [13, 236]
])

# Real football pitch coordinates
dst_points = np.float32([
    [0, 0],
    [105, 0],
    [105, 68],
    [0, 68]
])

matrix = cv2.getPerspectiveTransform(
    src_points,
    dst_points
)

GRID_COLS = 21
GRID_ROWS = 14


by_id = defaultdict(list)
for d in data:
    point = np.array([
        [d["foot_x"], d["foot_y"]]
    ], dtype=np.float32)
    point = np.array([point])
    transformed = cv2.perspectiveTransform(
        point,
        matrix
    )[0][0]

    pitch_x = transformed[0]
    pitch_y = transformed[1]

    d["pitch_x"] = float(pitch_x)
    d["pitch_y"] = float(pitch_y)


    by_id[d["id"]].append(d)

heatmaps = {}
for pid, records in by_id.items():

    grid = [
        [0]*GRID_COLS
        for _ in range(GRID_ROWS)
    ]
    for r in records:

        x = r["pitch_x"]
        y = r["pitch_y"]


        if 0 <= x <= 105 and 0 <= y <= 68:

            col = int(x / 105 * GRID_COLS)
            row = int(y / 68 * GRID_ROWS)


            col = min(col, GRID_COLS-1)
            row = min(row, GRID_ROWS-1)


            grid[row][col] += 1

    heatmaps[str(pid)] = grid



with open("heatmaps_pitch.json","w") as f:
    json.dump(heatmaps,f)

print(
    f"Pitch heatmaps built for {len(heatmaps)} players"
)