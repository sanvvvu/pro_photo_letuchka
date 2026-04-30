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


def update_exif(path, tag, value, out_path):
    img = Image.open(path)

    exif_dict = piexif.load(img.info.get("exif", b""))

    # всегда пишем в 0th (EXIF стандарт)
    exif_dict["0th"][int(tag)] = value.encode("utf-8")

    exif_bytes = piexif.dump(exif_dict)
    img.save(out_path, exif=exif_bytes)