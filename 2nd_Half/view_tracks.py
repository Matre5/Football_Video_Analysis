import cv2
from ultralytics import YOLO


model = YOLO("yolov8n.pt")

video_path = r"Mitus_INT/england_epl/2014-2015/2015-02-21 - 18-00 Crystal Palace 1 - 2 Arsenal/1_224p.mkv"


cap = cv2.VideoCapture(video_path)


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)


out = cv2.VideoWriter(
    "tracked_output.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)


results = model.track(
    source=video_path,
    device=0,
    classes=[0],
    tracker="bytetrack.yaml",
    conf=0.5,
    stream=True,
    persist=True,
    verbose=False
)


for r in results:

    frame = r.orig_img

    if r.boxes.id is not None:

        boxes = r.boxes.xyxy.cpu().numpy()
        ids = r.boxes.id.cpu().numpy()


        for box, track_id in zip(boxes, ids):

            x1, y1, x2, y2 = map(int, box)


            cv2.rectangle(
                frame,
                (x1,y1),
                (x2,y2),
                (0,255,0),
                2
            )


            cv2.putText(
                frame,
                f"ID {int(track_id)}",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )


    out.write(frame)


out.release()

print("Done! Saved as tracked_output.mp4")