import os
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_PATH = "models/model.pkl"


def extract_features(path):
    img = cv2.imread(str(path))
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
    X = [
        [100000, 120, 30, 900],
        [120000, 80, 10, 300],
        [150000, 200, 60, 2000],
        [90000,  100, 20, 500]
    ]

    y = [0, 1, 0, 1]

    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)


def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)


def predict_image(path):
    model = load_model()
    feat = np.array(extract_features(path)).reshape(1, -1)
    pred = model.predict(feat)[0]

    return {
        "edited": bool(pred)
    }