import cv2
import numpy as np
import os

def detect_copy_move(path):
    img = cv2.imread(str(path))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()

    kp, des = sift.detectAndCompute(gray, None)

    if des is None or len(des) < 2:
        return {
            "file": None,
            "matches": 0,
            "interpretation": "Недостаточно ключевых точек"
        }

    bf = cv2.BFMatcher()

    matches = bf.knnMatch(des, des, k=2)

    suspicious = []

    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            pt1 = kp[m.queryIdx].pt
            pt2 = kp[m.trainIdx].pt

            dist = np.linalg.norm(np.array(pt1) - np.array(pt2))

            if dist > 20:
                suspicious.append((pt1, pt2))

    out = img.copy()

    for p1, p2 in suspicious:
        cv2.line(
            out,
            (int(p1[0]), int(p1[1])),
            (int(p2[0]), int(p2[1])),
            (0, 0, 255),
            2
        )

    filename = "cmfd_" + os.path.basename(path)
    out_path = os.path.join("uploads", filename)

    cv2.imwrite(out_path, out)

    return {
        "file": filename,
        "matches": len(suspicious),
        "interpretation":
            "Обнаружены потенциальные клонированные области"
            if len(suspicious) > 10
            else "Подозрительных клонирований не найдено"
    }