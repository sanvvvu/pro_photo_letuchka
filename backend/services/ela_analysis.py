import cv2
import numpy as np
import os

def perform_ela(path, quality=90):
    original = cv2.imread(str(path))

    temp_path = "temp_ela.jpg"
    cv2.imwrite(temp_path, original, [cv2.IMWRITE_JPEG_QUALITY, quality])

    compressed = cv2.imread(temp_path)

    diff = cv2.absdiff(original, compressed)

    scale = 15
    ela = np.clip(diff * scale, 0, 255)

    filename = "ela_" + os.path.basename(path)
    out_path = os.path.join("uploads", filename)

    cv2.imwrite(out_path, ela)

    score = float(np.mean(diff))

    interpretation = (
        "Высокая вероятность локального редактирования"
        if score > 12
        else "Серьёзных аномалий компрессии не найдено"
    )

    return {
        "file": filename,
        "score": round(score, 2),
        "interpretation": interpretation
    }