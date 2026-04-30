# backend/services/compare.py
import cv2
import numpy as np

def compare_images(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    diff = cv2.absdiff(img1, img2)
    score = float(np.mean(diff))

    return {"difference_score": score}