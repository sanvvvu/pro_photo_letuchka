from PIL import Image
import piexif

def get_exif_data(path):
    img = Image.open(path)
    if "exif" not in img.info:
        return {"exif": None}
    return piexif.load(img.info["exif"])


def edit_simple_exif(input_path, output_path, model_name):
    img = Image.open(input_path)

    exif_dict = {"0th": {piexif.ImageIFD.Model: model_name.encode()}}
    exif_bytes = piexif.dump(exif_dict)

    img.save(output_path, exif=exif_bytes)