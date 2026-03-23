from fastapi import FastAPI, UploadFile, File
import tempfile
import shutil
import os

from extractor import run_ocr

app = FastAPI()

@app.post("/extract")
async def extract(file: UploadFile = File(...)):

    # preserve extension
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    result = run_ocr(tmp_path)

    os.remove(tmp_path)

    return result