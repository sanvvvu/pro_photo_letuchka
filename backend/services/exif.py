from PIL import Image
import piexif
import os

TAGS = {
    "Artist": 315,
    "Software": 305,
    "ImageDescription": 270,
    "Make": 271,
    "Model": 272,
    "Copyright": 33432
}


def get_exif_data(path):

    img = Image.open(path)

    result = {
        "Technical": {},
        "Description": {},
        "Administrative": {},
        "GPS": {}
    }

    result["Technical"]["File"] = os.path.basename(path)
    result["Technical"]["Format"] = img.format
    result["Technical"]["Mode"] = img.mode
    result["Technical"]["Width"] = img.width
    result["Technical"]["Height"] = img.height

    if "exif" not in img.info:
        return result

    exif_dict = piexif.load(img.info["exif"])

    for ifd_name in exif_dict:

        if isinstance(exif_dict[ifd_name], dict):

            for tag_id, value in exif_dict[ifd_name].items():

                try:
                    value = value.decode(errors="ignore")

                except:
                    pass

                result[ifd_name][str(tag_id)] = str(value)

    return result


def update_exif(path, ifd, tag_name, value):

    img = Image.open(path)

    exif_dict = {}

    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])

    else:
        exif_dict = {
            "0th": {},
            "Exif": {},
            "GPS": {},
            "1st": {},
            "thumbnail": None
        }

    if tag_name not in TAGS:

        return {
            "error":
            "Неизвестный тег"
        }

    tag_id = TAGS[tag_name]

    exif_dict[ifd][tag_id] = value.encode()

    exif_bytes = piexif.dump(exif_dict)

    out_name = "exif_" + os.path.basename(path)

    out_path = os.path.join(
        os.path.dirname(path),
        out_name
    )

    img.save(out_path, exif=exif_bytes)

    return {
        "file": out_name
    }