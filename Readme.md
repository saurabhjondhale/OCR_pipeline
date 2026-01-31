# OCR Pipeline

A FastAPI-based web application for PDF processing, text extraction, and OCR (Optical Character Recognition) conversion.

**Author:** Saurabh Jondhale

## Features

- 📄 Upload PDF files through a web interface
- 🔄 Multiple processing options:
  - Extract text from searchable PDFs
  - Convert image-based PDFs to searchable OCR PDFs
  - Full process (OCR + text extraction)
- 📝 View extracted text in a web interface
- 📥 Download processed PDFs and extracted text files
- 📋 Copy extracted text to clipboard

## Installation

### Prerequisites

- Python 3.12+
- Poetry (Python dependency manager)

### Setup with Poetry

1. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment:**

   ```bash
   # On Linux/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install Poetry (if not already installed):**

   ```bash
   pip install poetry
   ```

4. **Install project dependencies:**

   ```bash
   poetry install
   ```

## Running the Application

### Locally

```bash
# Make sure your virtual environment is activated
source .venv/bin/activate

# Run the FastAPI app
python app.py
```

The application will be available at `http://localhost:8000`

## Docker Setup

### Build the Docker Image

```bash
docker build -t ocr-pipeline . --network host
```

### Run the Docker Container

```bash
docker run -p 8000:8000 ocr-pipeline
```

If you encounter networking issues, try:

```bash
docker run --network host ocr-pipeline
```

The application will be available at `http://localhost:8000`

### Docker Features

The Dockerfile includes:

- Python 3.12 slim base image
- Tesseract OCR and related system dependencies
- PDF processing tools (ocrmypdf, ghostscript, poppler-utils)
- Image processing libraries (Pillow, libjpeg)
- Automatic Poetry dependency installation

## Project Structure

```
OCR_pipeline/
├── app.py                 # FastAPI application
├── Dockerfile            # Docker configuration
├── pyproject.toml        # Poetry dependencies
├── templates/
│   └── index.html        # Web interface
└── ocr/
    ├── __init__.py
    ├── extract_text.py   # Text extraction logic
    ├── ocr_pdf.py        # OCR conversion logic
    └── __pycache__/
```

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **pytesseract**: Tesseract OCR wrapper
- **ocrmypdf**: PDF OCR conversion
- **pdf2image**: PDF to image conversion
- **pypdf2**: PDF manipulation
- **Pillow**: Image processing

## Troubleshooting

### Tesseract Not Found

If you get "tesseract is not installed or it's not in your PATH" error:

- **Linux (Ubuntu/Debian):**

  ```bash
  sudo apt-get install tesseract-ocr
  ```

- **macOS:**

  ```bash
  brew install tesseract
  ```

- **Docker:** The Dockerfile includes all necessary dependencies

### File Upload Issues

Ensure the `uploads/` and `outputs/` directories exist and have proper permissions.

## License

MIT License
