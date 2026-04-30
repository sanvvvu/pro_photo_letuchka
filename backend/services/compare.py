import cv2
import numpy as np

def compare_images(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    if img1 is None or img2 is None:
        return {"difference_score": 0, "interpretation": "Ошибка загрузки"}

    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    diff = cv2.absdiff(img1, img2)
    score = float(np.mean(diff))

    return {
        "difference_score": round(score, 2),
        "interpretation": (
            "0-10: почти одинаковые\n"
            "10-50: небольшие изменения\n"
            "50+: сильная модификация"
        )
    }