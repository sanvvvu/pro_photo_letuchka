from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from services.ml_model import predict_image
from services.steganography import embed_file, extract_file
from services.compare import compare_images
from services.exif import get_exif_data, update_exif

app = FastAPI()

BASE = Path(__file__).resolve().parent.parent
UPLOAD = BASE / "uploads"
UPLOAD.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=BASE / "frontend"), name="static")


@app.get("/")
def home():
    return FileResponse(BASE / "frontend/index.html")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = UPLOAD / file.filename
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename}


@app.get("/image/{name}")
def image(name: str):
    return FileResponse(UPLOAD / name)


@app.post("/analyze")
def analyze(filename: str = Form(...)):
    path = UPLOAD / filename
    ml = predict_image(path)

    return {
        "result": "Изменено" if ml["edited"] else "Оригинал"
    }


@app.post("/stego/embed")
async def embed(file: UploadFile = File(...), filename: str = Form(...)):
    data = await file.read()

    out = UPLOAD / f"stego_{filename}"
    embed_file(UPLOAD / filename, out, data)

    return {"file": out.name}


@app.post("/stego/extract")
def extract(filename: str = Form(...)):
    data = extract_file(UPLOAD / filename)
    return {"text": data.decode(errors="ignore")}


@app.post("/compare")
async def compare(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    p1 = UPLOAD / file1.filename
    p2 = UPLOAD / file2.filename

    with open(p1, "wb") as f:
        shutil.copyfileobj(file1.file, f)
    with open(p2, "wb") as f:
        shutil.copyfileobj(file2.file, f)

    return compare_images(p1, p2)


@app.get("/exif")
def exif(filename: str):
    return get_exif_data(UPLOAD / filename)


@app.post("/exif/edit")
def exif_edit(filename: str = Form(...), tag: str = Form(...), value: str = Form(...)):
    out = UPLOAD / f"exif_{filename}"
    update_exif(UPLOAD / filename, out, tag, value)
    return {"file": out.name}