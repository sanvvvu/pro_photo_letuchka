import cv2
import numpy as np
import os

def analyze_cfa(path):
    img = cv2.imread(str(path))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    residual = cv2.absdiff(gray, blur)

    heatmap = cv2.applyColorMap(residual, cv2.COLORMAP_JET)

    filename = "cfa_" + os.path.basename(path)
    out_path = os.path.join("uploads", filename)

    cv2.imwrite(out_path, heatmap)

    variance = float(np.var(residual))

    interpretation = (
        "Обнаружены аномалии CFA-интерполяции"
        if variance > 120
        else "CFA структура выглядит однородной"
    )

    return {
        "file": filename,
        "variance": round(variance, 2),
        "interpretation": interpretation
    }