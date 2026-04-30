# backend/services/ml_model.py
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier

X = np.array([
    [100000, 120, 30],
    [200000, 50, 10]
])
y = np.array([0, 1])

model = RandomForestClassifier()
model.fit(X, y)


def predict_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    feat = np.array([
        img.size,
        np.mean(gray),
        np.std(gray)
    ]).reshape(1, -1)

    pred = model.predict(feat)[0]

    return {
        "edited": bool(pred)
    }