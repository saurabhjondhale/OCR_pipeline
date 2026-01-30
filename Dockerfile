FROM python:3.10-slim

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-all \
    ocrmypdf \
    poppler-utils \
    ghostscript \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean

WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
