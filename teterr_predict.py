from ultralytics import YOLO
import json

model = YOLO("yolov8n.pt")

results = model.track(
    source="Mitus_INT/england_epl/2014-2015/2015-02-21 - 18-00 Crystal Palace 1 - 2 Arsenal/1_224p.mkv",
    device=0,
    classes=[0],
    stream=True,
    verbose=False,
    persist=True
)

all_tracks = []

for frame_idx, r in enumerate(results):
    if r.boxes.id is None:
        continue
    
    for box, track_id, in zip(r.boxes.xywh, r.boxes.id):
        x, y, w, h = box.tolist()
        all_tracks.append(
            {
                "tracks": frame_idx,
                "id": int(track_id),
                "x": x,
                "y": y
            }
        )
        
with open("tracks.json", "w") as f:
    json.dump(all_tracks, f)