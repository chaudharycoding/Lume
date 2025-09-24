import numpy as np
from ultralytics import YOLO
import os
import shutil

class FireDetection:
    def __init__(self, model_path, conf=0.3, iou=0.6):
        self.model = YOLO(model_path)
        self.conf = conf
        self.iou = iou

    def detect_fire(self, video_path, save_output=True, augment=False, imgsz=416):
        # Set save directory to uploads/track folder
        save_dir = 'uploads'  # Set to uploads directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Get the original filename
        filename = os.path.basename(video_path)
        
        print(f"🔥 Processing video: {filename} with optimized settings for cloud deployment")
        
        # Run detection with optimized settings for Railway
        results = self.model.track(
            source=video_path, 
            conf=self.conf, 
            iou=self.iou, 
            augment=augment,      # Disabled for faster processing
            persist=True, 
            imgsz=imgsz,          # Reduced from 640 to 416 for faster processing
            save=save_output,
            project=save_dir,      # Save in uploads
            name='track',         # Save in track subdirectory
            save_txt=False,       # Don't save labels
            save_conf=False,      # Don't save confidences
            exist_ok=True,        # Overwrite existing files
            stream=True,          # Stream results to prevent RAM accumulation
            verbose=False,        # Reduce logging overhead
            device='cpu'          # Ensure CPU-only processing
        )
        
        processed_boxes = self.process_detections(results)
        
        # Analyze fire detection patterns
        consecutive_detections = 0
        max_consecutive = 0
        total_detections = 0
        total_frames = len(processed_boxes)
        
        for boxes in processed_boxes:
            if len(boxes) > 0:  # Fire detected in this frame
                consecutive_detections += 1
                total_detections += 1
                max_consecutive = max(max_consecutive, consecutive_detections)
            else:  # No fire in this frame
                consecutive_detections = 0
        
        # Calculate detection metrics
        detection_ratio = total_detections / total_frames if total_frames > 0 else 0
        
        # Consider it a fire if:
        # 1. We have at least 3 consecutive frames with fire OR
        # 2. Fire is detected in at least 15% of total frames
        is_fire = max_consecutive >= 3 or detection_ratio >= 0.15
        
        print(f"\nFire Detection Analysis:")
        print(f"Total Frames: {total_frames}")
        print(f"Frames with Fire: {total_detections}")
        print(f"Longest Consecutive Detection: {max_consecutive} frames")
        print(f"Detection Ratio: {detection_ratio:.2%}")
        
        if not is_fire and total_detections > 0:
            print("\n✅ Analysis Result: Controlled Fire Setting")
            print("While some fire was detected, the pattern suggests a controlled setting")
            print("(like a fireplace or fire pit) rather than an emergency situation.")
            print("This assessment is based on the limited and consistent nature of detections.")
        elif not is_fire:
            print("\n✅ Analysis Result: No Fire Detected")
            print("No significant fire patterns were detected in the video.")
        else:
            print("\n🚨 FIRE DETECTED - Emergency situation possible")
        
        print()  # Extra line for readability
        return processed_boxes, is_fire

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
