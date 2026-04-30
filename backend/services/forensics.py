# backend/services/forensics.py
import cv2
import numpy as np

def analyze_forensics(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return {
        "mean": float(np.mean(gray)),
        "std": float(np.std(gray)),
        "noise": float(np.var(gray))
    }