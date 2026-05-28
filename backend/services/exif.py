from PIL import Image
import piexif


EXIF_TAGS_INFO = {
    "0th": {
        271: "Модель камеры",
        272: "Производитель",
        306: "Дата изменения",
        305: "ПО",
        315: "Автор",
        33432: "Правообладатель"
    },
    "Exif": {
        36867: "Дата создания",
        36868: "Дата цифровизации"
    },
    "GPS": {
        1: "Широта (N/S)",
        2: "Широта",
        3: "Долгота (E/W)",
        4: "Долгота"
    }
}


def get_exif_data(path):
    img = Image.open(path)

    if "exif" not in img.info:
        return {"empty": True, "data": {}}

    exif = piexif.load(img.info["exif"])

    result = {}

    for ifd in exif:
        result[ifd] = {}

        for tag in EXIF_TAGS_INFO.get(ifd, {}):
            value = exif.get(ifd, {}).get(tag, None)

            if value is None:
                result[ifd][tag] = "—"
            else:
                try:
                    result[ifd][tag] = value.decode("utf-8")
                except:
                    result[ifd][tag] = str(value)

    return result


def update_exif(path, tag, value, out_path):
    img = Image.open(path)

    exif_dict = piexif.load(img.info.get("exif", b""))

    # пишем в 0th (безопасный дефолт)
    exif_dict["0th"][int(tag)] = str(value).encode("utf-8")

    exif_bytes = piexif.dump(exif_dict)
    img.save(out_path, exif=exif_bytes)