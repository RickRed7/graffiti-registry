import os
import cv2
import numpy as np
from ultralytics import YOLO

class GraffitiDetector:
    def __init__(self, model_path="models/graffiti_yolo.pt", confidence_threshold=0.50):
        self.confidence_threshold = confidence_threshold
        if not os.path.exists(model_path):
            self.model = YOLO("yolov8n.pt")
        else:
            self.model = YOLO(model_path)

    def extract_tags(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image at {image_path}")
        results = self.model(image, verbose=False)[0]
        detected_crops = []
        for box in results.boxes:
            confidence = float(box.conf[0])
            if confidence < self.confidence_threshold:
                continue
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = xyxy
            cropped_tag = image[y1:y2, x1:x2]
            detected_crops.append({
                "crop": cropped_tag,
                "bbox": (x1, y1, x2, y2),
                "confidence": confidence
            })
        return detected_crops
