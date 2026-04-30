from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from services.image_processing import *
from services.exif import *
from services.steganography import *
from services.forensics import analyze_forensics
from services.ml_model import predict_image
from services.dct_analysis import analyze_dct
from services.heatmap import generate_heatmap_image
from services.compare import compare_images

app = FastAPI()

UPLOAD_DIR = Path("../uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="../frontend"), name="static")


@app.get("/")
def index():
    return FileResponse("../frontend/index.html")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = UPLOAD_DIR / file.filename
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename}


@app.get("/image/{name}")
def get_image(name: str):
    return FileResponse(UPLOAD_DIR / name)


@app.post("/process")
def process(filename: str, action: str):
    img = load_image(str(UPLOAD_DIR/filename))

    if action == "blur":
        img = gaussian_blur(img)
    elif action == "sharpen":
        img = sharpen(img)

    out = UPLOAD_DIR / f"edit_{filename}"
    img.save(out)
    return FileResponse(out)


@app.get("/exif")
def exif(filename: str):
    return get_exif_data(str(UPLOAD_DIR / filename))


@app.post("/exif/edit")
def exif_edit(data: dict):
    filename = data["filename"]
    new_model = data["model"]

    in_path = str(UPLOAD_DIR / filename)
    out_path = str(UPLOAD_DIR / f"exif_{filename}")

    edit_simple_exif(in_path, out_path, new_model)
    return {"file": f"exif_{filename}"}


@app.post("/stego/embed")
def stego_embed(data: dict):
    filename = data["filename"]
    text = data["text"]

    in_path = str(UPLOAD_DIR / filename)
    out_path = str(UPLOAD_DIR / f"stego_{filename}")

    embed_text_in_image(in_path, out_path, text)
    return {"file": f"stego_{filename}"}


@app.post("/stego/extract")
def stego_extract(data: dict):
    filename = data["filename"]
    text = extract_text_from_image(str(UPLOAD_DIR / filename))
    return {"text": text}


@app.post("/compare")
def compare(file1: str, file2: str):
    return compare_images(
        str(UPLOAD_DIR / file1),
        str(UPLOAD_DIR / file2)
    )


@app.post("/analyze")
def analyze(filename: str):
    path = str(UPLOAD_DIR / filename)

    heat = generate_heatmap_image(path)
    ml = predict_image(path)

    return {
        "result": "ИЗМЕНЕНО" if ml["edited"] else "ОРИГИНАЛ",
        "ml": ml,
        "forensics": analyze_forensics(path),
        "dct": analyze_dct(path),
        "heatmap": f"/image/{heat}"
    }