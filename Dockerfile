FROM python:3.12-slim

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-all \
    libtesseract-dev \
    ocrmypdf \
    poppler-utils \
    ghostscript \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry

# Copy project files
COPY . .

# Install Python dependencies using Poetry
RUN poetry install --no-interaction --no-ansi --no-cache

EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "localhost", "--port", "8000"]
