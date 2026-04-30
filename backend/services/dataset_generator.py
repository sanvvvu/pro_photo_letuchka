# backend/services/dataset_generator.py
import cv2
import os
import numpy as np
from PIL import Image

def generate_dataset(input_dir="uploads", out_dir="dataset"):
    os.makedirs(out_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        path = os.path.join(input_dir, file)

        img = cv2.imread(path)

        # original
        cv2.imwrite(os.path.join(out_dir, "orig_" + file), img)

        # compressed (simulated attack)
        cv2.imwrite(os.path.join(out_dir, "comp_" + file),
                    cv2.resize(img, (128, 128)))