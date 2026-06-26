from ultralytics import YOLO

model = YOLO("yolov8n.pt")
# model.to("cuda") #running on GPU instead of CPU
# print(model.device)

results = model.predict(
    source = "Mitus_INT/england_epl/2014-2015/2015-02-21 - 18-00 Crystal Palace 1 - 2 Arsenal/1_224p.mkv",
    device = 0,
    save = True,
    classes =[0],
    stream=True,
    verbose=False
)

for r in results:
    pass 