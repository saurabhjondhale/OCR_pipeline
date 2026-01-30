from flask import Flask, render_template, request, send_file
import os
from scripts.ocr_pdf import convert_to_ocr
from scripts.extract_text import extract_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    file = request.files["pdf"]
    task = request.form["task"]

    # Save uploaded file
    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    ocr_path = None
    text_path = None

    # Run OCR PDF conversion
    if task in ["ocr", "full"]:
        ocr_path = convert_to_ocr(upload_path)

    # Run text extraction
    if task in ["text", "full"]:
        pdf_for_text = ocr_path if task == "full" else upload_path
        text_path = extract_text(pdf_for_text)

    return render_template(
        "result.html",
        ocr_path=ocr_path,
        text_path=text_path
    )

@app.route("/download")
def download():
    file_path = request.args.get("file")
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
