import os
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_PATH = "models/model.pkl"


def extract_features(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return [
        img.size,
        np.mean(gray),
        np.std(gray),
        np.var(gray)
    ]


def train_model(dataset_path="dataset"):
    X, y = [], []

    for file in os.listdir(dataset_path):
        path = os.path.join(dataset_path, file)

        features = extract_features(path)

        if file.startswith("orig"):
            label = 0
        else:
            label = 1

        X.append(features)
        y.append(label)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)


def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)


model = load_model()


def predict_image(path):
    features = np.array(extract_features(path)).reshape(1, -1)
    pred = model.predict(features)[0]

    return {"edited": bool(pred)}