import json

with open("tracks_speed.json") as f:
    data = json.load(f)

xs = [d["foot_x"] for d in data]
ys = [d["foot_y"] for d in data]

print("X range:", min(xs), max(xs))
print("Y range:", min(ys), max(ys))

print("Sample coordinates:")
for d in data[:10]:
    print(
        d["foot_x"],
        d["foot_y"]
    )