import os
import cv2
import numpy as np

class TagMatcher:
    def __init__(self, database_dir="data/database/", similarity_threshold=0.75):
        self.database_dir = database_dir
        self.similarity_threshold = similarity_threshold

    def compute_embedding(self, img_array):
        resized = cv2.resize(img_array, (128, 128))
        hist_b = cv2.calcHist([resized], [0], None, [64], [0, 256])
        hist_g = cv2.calcHist([resized], [1], None, [64], [0, 256])
        hist_r = cv2.calcHist([resized], [2], None, [64], [0, 256])
        feature_vector = np.concatenate((hist_b, hist_g, hist_r), axis=0)
        cv2.normalize(feature_vector, feature_vector)
        return feature_vector.flatten()

    def find_matches(self, target_crop):
        target_vector = self.compute_embedding(target_crop)
        best_match = None
        highest_score = -1.0
        if not os.path.exists(self.database_dir):
            return "Unknown_Moniker", 0.0
        for file_name in os.listdir(self.database_dir):
            if file_name.endswith(('.png', '.jpg', '.jpeg')):
                db_img_path = os.path.join(self.database_dir, file_name)
                db_image = cv2.imread(db_img_path)
                if db_image is None:
                    continue
                db_vector = self.compute_embedding(db_image)
                similarity = np.dot(target_vector, db_vector) / (
                    np.linalg.norm(target_vector) * np.linalg.norm(db_vector)
                )
                if similarity > highest_score:
                    highest_score = similarity
                    best_match = os.path.splitext(file_name)[0]
        if highest_score >= self.similarity_threshold:
            return best_match, highest_score
        return "Unknown_Moniker", highest_score
