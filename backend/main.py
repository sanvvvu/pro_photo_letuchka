from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from services.image_processing import load_image, gaussian_blur, sharpen
from services.exif import get_exif_data, update_exif
from services.compare import compare_images
from services.forensics import analyze_forensics
from services.ml_model import predict_image
from services.dct_analysis import analyze_dct
from services.heatmap import generate_heatmap_image
from services.plot import histogram_plot

from services.ela_analysis import perform_ela
from services.cmfd_analysis import detect_copy_move
from services.cfa_analysis import analyze_cfa

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
        return {"error": "Файл не найден"}

    return FileResponse(path)


# ---------- PROCESS ----------
@app.post("/process")
def process(filename: str = Form(...), action: str = Form(...)):
    path = UPLOAD_DIR / filename

    img = load_image(path)

    if action == "blur":
        img = gaussian_blur(img)

    elif action == "sharpen":
        img = sharpen(img)

    out_name = f"edit_{filename}"

    out_path = UPLOAD_DIR / out_name

    img.save(out_path)

    return {"file": out_name}


# ---------- RESET ----------
@app.post("/reset")
def reset_image(filename: str = Form(...)):
    return {"file": filename}


# ---------- EXIF ----------
@app.get("/exif")
def exif(filename: str):
    return get_exif_data(UPLOAD_DIR / filename)


@app.post("/exif/edit")
def exif_edit(
    filename: str = Form(...),
    ifd: str = Form(...),
    tag: str = Form(...),
    value: str = Form(...)
):
    path = UPLOAD_DIR / filename

    result = update_exif(path, ifd, tag, value)

    return result


# ---------- COMPARE ----------
@app.post("/compare")
async def compare(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
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

    forensic = analyze_forensics(path)

    dct = analyze_dct(path)

    return {
        "result":
            "Обнаружены признаки редактирования"
            if ml["edited"]
            else "Сильных признаков редактирования не найдено",

        "confidence": ml["confidence"],

        "explanation":
            "ML-анализ использует статистику шума, "
            "дисперсию пикселей, DCT-признаки "
            "и цифровые артефакты.",

        "noise": forensic["noise"],
        "mean": forensic["mean"],
        "std": forensic["std"],

        "dct_low": dct["low_freq"],
        "dct_high": dct["high_freq"],

        "heatmap": f"/image/{heat}"
    }


# ---------- HISTOGRAM ----------
@app.post("/plot")
def plot(filename: str = Form(...)):
    file = histogram_plot(UPLOAD_DIR / filename)

    return {
        "plot": f"/image/{file}"
    }


# ---------- ELA ----------
@app.post("/ela")
def ela(filename: str = Form(...)):
    result = perform_ela(UPLOAD_DIR / filename)

    return {
        "image": f"/image/{result['file']}",
        "score": result["score"],
        "interpretation": result["interpretation"]
    }


# ---------- CMFD ----------
@app.post("/cmfd")
def cmfd(filename: str = Form(...)):
    result = detect_copy_move(UPLOAD_DIR / filename)

    return {
        "image": f"/image/{result['file']}",
        "matches": result["matches"],
        "interpretation": result["interpretation"]
    }


# ---------- CFA ----------
@app.post("/cfa")
def cfa(filename: str = Form(...)):
    result = analyze_cfa(UPLOAD_DIR / filename)

    return {
        "image": f"/image/{result['file']}",
        "variance": result["variance"],
        "interpretation": result["interpretation"]
    }


# ---------- SAVE ----------
@app.post("/save")
def save(
    filename: str = Form(...),
    format: str = Form(...)
):
    img = load_image(UPLOAD_DIR / filename)

    out = f"saved_{filename.split('.')[0]}.{format.lower()}"

    path = UPLOAD_DIR / out

    img.save(path, format=format)

    return {"file": out}


# ---------- DOWNLOAD ----------
@app.get("/download/{filename}")
def download(filename: str):
    return FileResponse(
        UPLOAD_DIR / filename,
        filename=filename
    )