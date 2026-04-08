from fastapi import FastAPI, UploadFile, File
import tempfile, shutil, os

from ocr.paddle import run_ocr
from processing.line_builder import build_lines
from processing.normalize import normalize_lines
from processing.correction import correct_line, load_names
from processing.extractor import extract_fields
from processing.validator import validate, confidence

app = FastAPI()
NAMES = load_names()


def save_temp(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        return tmp.name


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    path = save_temp(file)

    try:
        # STEP 1 — OCR
        blocks = run_ocr(path)

        # STEP 2 — LINE BUILDER
        lines = build_lines(blocks)

        # STEP 3 — NORMALIZATION
        normalized = normalize_lines(lines)

        # STEP 4 — CORRECTION
        try:
            corrected = [correct_line(l, NAMES) for l in normalized]
        except Exception as e:
            print("CORRECTION ERROR:", e)
            corrected = []
        print("CORRECTED:", corrected)

        # STEP 5 — EXTRACTION
        fields = extract_fields(corrected, NAMES)

        # STEP 6 — VALIDATION
        validated = validate(fields)
        score = confidence(validated)

        return {
            "fields": validated,
            "confidence": score
        }

    finally:
        os.remove(path)