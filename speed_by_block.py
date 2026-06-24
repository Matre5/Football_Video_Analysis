import json
from collections import defaultdict

with open("tracks_speed.json") as f:
    data = json.load(f)

FPS = 25
BLOCK_MINUTES = 15
BLOCK_FRAMES = BLOCK_MINUTES * 60 * FPS   # 15 min * 60 sec * 25 frames/sec = 22,500

MIN_ENTRIES_PER_BLOCK = 30   # roughly 1+ second worth of real samples — below this, too thin to trust

by_id = defaultdict(list)
for d in data:
    by_id[d["id"]].append(d)

player_blocks = defaultdict(dict)

for pid, records in by_id.items():
    for r in records:
        block_num = r["frame"] // BLOCK_FRAMES
        player_blocks[pid].setdefault(block_num, []).append(r["speed_mps"])

block_averages = []

for pid, blocks in player_blocks.items():
    for block_num, speeds in blocks.items():
        if len(speeds) < MIN_ENTRIES_PER_BLOCK:
            continue
        avg_speed = sum(speeds) / len(speeds)
        block_averages.append({
            "id": pid,
            "block": block_num,
            "avg_speed": avg_speed,
            "samples": len(speeds),
        })

with open("speed_by_block.json", "w") as f:
    json.dump(block_averages, f)

print(f"Total player-block entries: {len(block_averages)}")