from PIL import Image
import piexif

def get_exif_data(path):
    img = Image.open(path)
    if "exif" not in img.info:
        return {}
    exif = piexif.load(img.info["exif"])

    readable = {}
    for ifd in exif:
        readable[ifd] = {}
        for tag, val in exif[ifd].items():
            readable[ifd][str(tag)] = str(val)
    return readable


def update_exif(path, new_exif, out):
    img = Image.open(path)

    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}}

    for ifd in new_exif:
        for tag, val in new_exif[ifd].items():
            exif_dict[ifd][int(tag)] = val.encode()

    exif_bytes = piexif.dump(exif_dict)
    img.save(out, exif=exif_bytes)