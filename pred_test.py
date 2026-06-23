from ultralytics import YOLO

model = YOLO('yolov8n')

results = model.track(
    source="clip_test.mkv",
    device = 0,
    classes=[0],
    save=True
)

