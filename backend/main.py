from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from services.image_processing import load_image, gaussian_blur, sharpen
from services.exif import get_exif_data, update_exif
from services.steganography import embed_file, extract_file
from services.compare import compare_images
from services.forensics import analyze_forensics
from services.ml_model import predict_image
from services.dct_analysis import analyze_dct
from services.heatmap import generate_heatmap_image

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "frontend/index.html")


# ---------- UPLOAD ----------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = UPLOAD_DIR / file.filename
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename}


@app.get("/image/{name}")
def get_image(name: str):
    return FileResponse(UPLOAD_DIR / name)


# ---------- PROCESS ----------
@app.post("/process")
def process(filename: str = Form(...), action: str = Form(...)):
    img = load_image(UPLOAD_DIR / filename)

    if action == "blur":
        img = gaussian_blur(img)
    elif action == "sharpen":
        img = sharpen(img)

    out_name = f"edit_{filename}"
    out_path = UPLOAD_DIR / out_name
    img.save(out_path)

    return {"file": out_name}


# ---------- EXIF ----------
@app.get("/exif")
def exif(filename: str):
    return get_exif_data(UPLOAD_DIR / filename)


@app.post("/exif/edit")
def exif_edit(filename: str = Form(...), tag: str = Form(...), value: str = Form(...)):
    out_name = f"exif_{filename}"
    out_path = UPLOAD_DIR / out_name

    update_exif(UPLOAD_DIR / filename, {"0th": {tag: value}}, out_path)

    return {"file": out_name}


# ---------- STEGO ----------
@app.post("/stego/embed")
async def stego_embed(file: UploadFile = File(...), filename: str = Form(...)):
    data = await file.read()

    out_name = f"stego_{filename}"
    embed_file(UPLOAD_DIR / filename, UPLOAD_DIR / out_name, data)

    return {"file": out_name}


@app.post("/stego/extract")
def stego_extract(filename: str = Form(...)):
    data = extract_file(UPLOAD_DIR / filename)
    return {"text": data.decode(errors="ignore")}


# ---------- COMPARE ----------
@app.post("/compare")
async def compare(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    p1 = UPLOAD_DIR / file1.filename
    p2 = UPLOAD_DIR / file2.filename

    with open(p1, "wb") as f:
        shutil.copyfileobj(file1.file, f)
    with open(p2, "wb") as f:
        shutil.copyfileobj(file2.file, f)

    return compare_images(p1, p2)


# ---------- ANALYZE ----------
@app.post("/analyze")
def analyze(filename: str = Form(...)):
    path = UPLOAD_DIR / filename

    heat = generate_heatmap_image(path)
    ml = predict_image(path)

    return {
        "result": "Изображение изменено" if ml["edited"] else "Изображение оригинальное",
        "explanation": "Анализ выполнен по статистике пикселей, шуму и структуре JPEG",
        "heatmap": f"/image/{heat}"
    }