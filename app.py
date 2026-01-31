from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

from ocr.ocr_pdf import convert_to_ocr, IMAGE_EXTENSIONS
from ocr.extract_text import extract_text

app = FastAPI()

UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)


@app.get("/")
async def index():
    return FileResponse("templates/index.html", media_type="text/html")


@app.post("/process")
async def process(pdf: UploadFile = File(...), task: str = Form(...)):
    if not UPLOAD_FOLDER.exists():
        UPLOAD_FOLDER.mkdir(parents=True)

    upload_path = UPLOAD_FOLDER / pdf.filename

    contents = await pdf.read()
    with open(upload_path, "wb") as f:
        f.write(contents)

    ocr_path = None
    text_path = None
    extracted_text = ""

    # Check if file is an image or PDF
    file_ext = Path(upload_path).suffix.lower()
    is_image = file_ext in IMAGE_EXTENSIONS

    # Run OCR PDF conversion (skip for images)
    if task in ["ocr", "full"] and not is_image:
        ocr_path = convert_to_ocr(str(upload_path))

    # Run text extraction
    if task in ["text", "full"]:
        # For images or if OCR failed, use original file
        if is_image:
            pdf_for_text = str(upload_path)
        else:
            pdf_for_text = ocr_path if ocr_path else str(upload_path)

        text_path = extract_text(pdf_for_text)

        # Read the extracted text file
        if text_path and Path(text_path).exists():
            with open(text_path, "r") as f:
                extracted_text = f.read()

    return JSONResponse(
        {"ocr_path": ocr_path, "text_path": text_path, "extracted_text": extracted_text}
    )


@app.get("/download")
async def download(file: str):
    file_path = Path(file)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path, media_type="application/octet-stream", filename=file_path.name
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
