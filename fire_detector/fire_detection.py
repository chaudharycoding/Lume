import numpy as np
from ultralytics import YOLO

class FireDetection:
    def __init__(self, model_path, conf=0.3, iou=0.6):
        self.model = YOLO(model_path)
        self.conf = conf
        self.iou = iou

    def detect_fire(self, video_path, save_output=True, augment=True, imgsz=640):
        results = self.model.track(source=video_path, conf=self.conf, iou=self.iou, augment=augment, persist=True, imgsz=imgsz, save=save_output)
        processed_boxes = self.process_detections(results)
        return processed_boxes

    def process_detections(self, results):
        all_boxes = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else []
            if boxes.size > 0:
                boxes = self.merge_detections(boxes)
            all_boxes.append(boxes)
        return all_boxes

    def merge_detections(self, boxes, iou_thresh=0.5):
        merged = []
        for box in boxes:
            x1, y1, x2, y2 = box[:4]
            merged_box = None
            for m in merged:
                if self.iou_score(m, box) > iou_thresh:
                    merged_box = [min(m[0], x1), min(m[1], y1), max(m[2], x2), max(m[3], y2)]
                    m[0], m[1], m[2], m[3] = merged_box
                    break
            if merged_box is None:
                merged.append(np.array([x1, y1, x2, y2]))
        return np.array(merged)

    def iou_score(self, box1, box2):
        x1, y1, x2, y2 = box1
        x1g, y1g, x2g, y2g = box2
        inter_x1 = max(x1, x1g)
        inter_y1 = max(y1, y1g)
        inter_x2 = min(x2, x2g)
        inter_y2 = min(y2, y2g)
        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x2g - x1g) * (y2g - y1g)
        union_area = box1_area + box2_area - inter_area
        return inter_area / union_area if union_area > 0 else 0
