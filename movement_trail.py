import cv2
import json
from collections import defaultdict

# -----------------------
# Load tracks
# -----------------------
with open("tracks_filtered.json") as f:
    data = json.load(f)

# group by id
tracks = defaultdict(list)

for d in data:
    tracks[d["id"]].append(d)

# sort each track by frame
for tid in tracks:
    tracks[tid].sort(key=lambda x: x["frame"])

# -----------------------
# Video input
# -----------------------
video_path = "Mitus_INT/england_epl/2014-2015/2015-02-21 - 18-00 Crystal Palace 1 - 2 Arsenal/1_224p.mkv"
cap = cv2.VideoCapture(video_path)

fps = int(cap.get(cv2.CAP_PROP_FPS))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(
    "output_trails.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (w, h)
)

# store history
history = defaultdict(list)

frame_idx = 0

# -----------------------
# MAIN LOOP
# -----------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # draw tracks that exist at this frame
    for tid, tlist in tracks.items():

        # find detections for this frame
        for t in tlist:
            if t["frame"] == frame_idx:

                x, y, bw, bh = t["x"], t["y"], t["w"], t["h"]

                cx = int(x)
                cy = int(y)

                # store history
                history[tid].append((cx, cy))

                # draw box
                cv2.rectangle(
                    frame,
                    (int(x - bw/2), int(y - bh/2)),
                    (int(x + bw/2), int(y + bh/2)),
                    (0, 255, 0),
                    2
                )

    # draw trails
    for tid, points in history.items():
        for i in range(1, len(points)):
            cv2.line(frame, points[i-1], points[i], (0, 0, 255), 2)

    out.write(frame)
    frame_idx += 1

cap.release()
out.release()

print("Done: output_trails.mp4 saved")