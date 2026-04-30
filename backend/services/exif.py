from PIL import Image
import piexif


def get_exif_data(path):
    img = Image.open(path)

    if "exif" not in img.info:
        return {"message": "EXIF отсутствует"}

    exif = piexif.load(img.info["exif"])

    result = {}

    for ifd in exif:
        result[ifd] = {}
        for tag, val in exif[ifd].items():
            result[ifd][str(tag)] = str(val)

    return result


def update_exif(path, out, tag, value):
    img = Image.open(path)

    exif_dict = piexif.load(img.info.get("exif", b""))

    try:
        exif_dict["0th"][int(tag)] = str(value).encode()
    except:
        pass

    exif_bytes = piexif.dump(exif_dict)
    img.save(out, exif=exif_bytes)