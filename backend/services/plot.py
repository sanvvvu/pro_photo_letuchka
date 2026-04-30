# backend/services/plot.py
import cv2
import matplotlib.pyplot as plt
import os

def histogram_plot(path):
    img = cv2.imread(path, 0)

    plt.figure()
    plt.hist(img.ravel(), bins=256)

    out = "uploads/hist.png"
    plt.savefig(out)
    plt.close()

    return "hist.png"