# backend/services/image_processing.py
from PIL import Image, ImageFilter

def load_image(path):
    return Image.open(path).convert("RGB")

def gaussian_blur(img, radius=2):
    return img.filter(ImageFilter.GaussianBlur(radius))

def sharpen(img):
    return img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))

def save_image(img, path, format):
    img.save(path, format=format)