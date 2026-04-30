# backend/services/steganography.py
from PIL import Image

def embed_file(input_path, output_path, file_bytes):
    img = Image.open(input_path)
    data = ''.join(format(b, '08b') for b in file_bytes) + '1111111111111110'

    pixels = list(img.getdata())
    new_pixels = []

    bit_idx = 0

    for pixel in pixels:
        r, g, b = pixel
        if bit_idx < len(data):
            r = (r & ~1) | int(data[bit_idx]); bit_idx+=1
        if bit_idx < len(data):
            g = (g & ~1) | int(data[bit_idx]); bit_idx+=1
        if bit_idx < len(data):
            b = (b & ~1) | int(data[bit_idx]); bit_idx+=1
        new_pixels.append((r,g,b))

    img.putdata(new_pixels)
    img.save(output_path)


def extract_file(path):
    img = Image.open(path)
    bits = ""

    for pixel in img.getdata():
        for val in pixel[:3]:
            bits += str(val & 1)

    bytes_out = []
    for i in range(0,len(bits),8):
        byte = bits[i:i+8]
        if byte == '11111111':
            break
        bytes_out.append(int(byte,2))

    return bytes(bytes_out)