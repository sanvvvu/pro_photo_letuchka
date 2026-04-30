# backend/services/steganography.py
from PIL import Image

def _gen_binary_list(data: str) -> list:
    """
    Преобразует строку в список бинарных строк по 8 бит на символ.
    """
    return [format(ord(c), '08b') for c in data]

def embed_text_in_image(input_path: str, output_path: str, secret: str) -> None:
    """
    Встраивает секретный текст в изображение, изменяя LSB цветовых каналов.
    """
    img = Image.open(input_path)
    binary_list = _gen_binary_list(secret)
    data_bits = "".join(binary_list)
    data_bits += '00000000'  # добавим нулевой завершающий байт
    img_data = iter(img.getdata())

    new_pixels = []
    bit_idx = 0
    for pixel in img_data:
        pix = list(pixel)
        for n in range(3):  # для каждого канала (R,G,B)
            if bit_idx < len(data_bits):
                bit = int(data_bits[bit_idx])
                # Меняем LSB: если текущий LSB не совпадает с bit, меняем число на противоположное (±1)
                if pix[n] % 2 != bit:
                    if pix[n] == 255:
                        pix[n] -= 1
                    else:
                        pix[n] += 1
                bit_idx += 1
        new_pixels.append(tuple(pix))
    img.putdata(new_pixels)
    img.save(output_path)

def extract_text_from_image(image_path: str) -> str:
    """
    Извлекает скрытый текст из изображения, считывая LSB каналов.
    """
    img = Image.open(image_path)
    bits = ""
    for pixel in img.getdata():
        for n in range(3):
            bits += str(pixel[n] % 2)  # извлекаем LSB каждого канала
    # Разбиваем на байты и конвертируем до первого 00000000
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == '00000000':
            break
        chars.append(chr(int(byte, 2)))
    return "".join(chars)
