# backend/services/image_processing.py
from PIL import Image, ImageFilter
import numpy as np
import cv2

def to_grayscale(image_path: str) -> Image.Image:
    """
    Конвертирует изображение в оттенки серого.
    """
    img = Image.open(image_path).convert('L')  # convert to grayscale【4†L250-L254】
    return img

def gaussian_blur(image: Image.Image, radius: float = 2.0) -> Image.Image:
    """
    Применяет гауссово размытие к изображению.
    """
    return image.filter(ImageFilter.GaussianBlur(radius))  # Gaussian blur【12†L45-L48】

def sharpen(image: Image.Image, times: int = 1) -> Image.Image:
    """
    Повышает резкость изображения (можно применять фильтр несколько раз).
    """
    for _ in range(times):
        image = image.filter(ImageFilter.SHARPEN)  # sharpen filter【14†L97-L100】
    return image

def resize(image: Image.Image, width: int, height: int) -> Image.Image:
    """
    Изменяет размер изображения до width×height.
    """
    return image.resize((width, height), Image.LANCZOS)  # resize【16†L42-L46】
