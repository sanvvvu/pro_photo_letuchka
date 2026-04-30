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
from services.plot import histogram_plot

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
    path = UPLOAD_DIR / name
    if not path.exists():
        return {"error": "not found"}
    return FileResponse(path)


# ---------- PROCESS ----------
@app.post("/process")
def process(filename: str = Form(...), action: str = Form(...)):
    img = load_image(UPLOAD_DIR / filename)

    if action == "blur":
        img = gaussian_blur(img)
    elif action == "sharpen":
        img = sharpen(img)

    out = UPLOAD_DIR / f"edit_{filename}"
    img.save(out)

    return {"file": f"edit_{filename}"}


# ---------- EXIF ----------
@app.get("/exif")
def exif(filename: str):
    return get_exif_data(UPLOAD_DIR / filename)


@app.post("/exif/edit")
def exif_edit(filename: str = Form(...), tag: str = Form(...), value: str = Form(...)):
    out = UPLOAD_DIR / f"exif_{filename}"
    update_exif(UPLOAD_DIR / filename, {"0th": {tag: value}}, out)
    return {"file": f"exif_{filename}"}


# ---------- STEGO ----------
@app.post("/stego/embed")
async def embed(file: UploadFile = File(...), filename: str = Form(...)):
    data = await file.read()

    out = UPLOAD_DIR / f"stego_{filename}"
    embed_file(UPLOAD_DIR / filename, out, data)

    return {"file": f"stego_{filename}"}


@app.post("/stego/extract")
def extract(filename: str = Form(...)):
    text = extract_file(UPLOAD_DIR / filename).decode(errors="ignore")
    return {"text": text}


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
        "result": "Изменено" if ml["edited"] else "Оригинал",
        "confidence": ml["confidence"],
        "explanation": "Анализ пикселей + шум + ML классификация",
        "heatmap": f"/image/{heat}"
    }


# ---------- SAVE ----------
@app.post("/save")
def save(filename: str = Form(...), format: str = Form(...)):
    img = load_image(UPLOAD_DIR / filename)

    out = f"saved_{filename.split('.')[0]}.{format.lower()}"
    path = UPLOAD_DIR / out

    img.save(path, format=format)

    return {"file": out}