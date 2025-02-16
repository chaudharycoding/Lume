from ultralytics import YOLO 

model = YOLO('weights/new_fire_detection.pt')

result = model.track('input_videos/12368500_2160_3240_30fps.mp4', 
                     conf=0.3, 
                     iou=0.6,  # Increase IoU to merge close detections
                     agnostic_nms=True, 
                     persist=True, 
                     save=True)
