import cv2
import numpy as np

def compare_images(p1, p2):
    img1 = cv2.imread(str(p1))
    img2 = cv2.imread(str(p2))

    if img1 is None or img2 is None:
        return {"error": "Файл не найден"}

    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    diff = cv2.absdiff(img1, img2)
    score = float(np.mean(diff))

    return {
        "difference_score": score,
        "meaning": "0 = одинаковые изображения, чем больше — тем сильнее различия"
    }