# backend/services/heatmap.py
import cv2
import numpy as np
import os

def generate_heatmap_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    diff = cv2.absdiff(gray, blur)

    heatmap = cv2.applyColorMap(diff, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    filename = "heatmap_" + os.path.basename(path)
    out_path = os.path.join("../uploads", filename)

    cv2.imwrite(out_path, overlay)

    return filename