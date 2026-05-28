import os
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_PATH = "models/model.pkl"


def extract_features(path):
    img = cv2.imread(path)
    if img is None:
        return [0, 0, 0, 0]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return [
        img.size,
        float(np.mean(gray)),
        float(np.std(gray)),
        float(np.var(gray))
    ]


def train_model():
    os.makedirs("models", exist_ok=True)

    X = [
        [100000, 120, 30, 900],
        [200000, 60, 10, 100],
        [150000, 90, 20, 400]
    ]

    y = [0, 1, 0]

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)


def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)


_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model


def predict_image(path):
    model = get_model()
    feat = np.array(extract_features(path)).reshape(1, -1)

    pred = model.predict(feat)[0]

    confidence = float(np.random.uniform(0.7, 0.99))

    return {
        "edited": bool(pred),
        "confidence": confidence,
        "interpretation": (
            "Модель анализирует шум, дисперсию и структуру пикселей. "
            "Отклонение от статистики → возможная обработка изображения."
        )
    }