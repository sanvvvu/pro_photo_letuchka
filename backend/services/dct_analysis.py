# backend/services/dct_analysis.py
import cv2
import numpy as np

def analyze_dct(path):
    img = cv2.imread(path, 0)
    img = cv2.resize(img, (256, 256))

    dct = cv2.dct(np.float32(img))

    return {
        "low_freq": float(np.mean(dct[:20, :20])),
        "high_freq": float(np.mean(dct[-20:, -20:])),
    }