import os
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract  # type: ignore
from PyPDF2 import PdfReader
from PIL import Image

from ocr import LANGUAGES

# Supported image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


def extract_text(input_file_path):
    """
    Extracts OCR text from a PDF or image file and saves as .txt
    Returns the path to the text file.
    """

    # Make output folder
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    # Get output filename
    base = os.path.splitext(os.path.basename(input_file_path))[0]
    output_path = os.path.join(output_folder, f"{base}_extracted.txt")

    # Check file type
    file_ext = Path(input_file_path).suffix.lower()
    is_image = file_ext in IMAGE_EXTENSIONS

    full_text = ""

    # Handle image files
    if is_image:
        try:
            print(f"📷 Processing image: {input_file_path}")
            image = Image.open(input_file_path)

            # OCR extraction
            text = pytesseract.image_to_string(
                image,
                lang=LANGUAGES,
                config="--psm 6",
            )

            full_text += text
            print(f"✅ Image processed successfully")

        except Exception as e:
            print(f"❌ Failed to process image: {e}")
            raise e

    # Handle PDF files
    else:
        # Try reading number of pages
        try:
            reader = PdfReader(input_file_path)
            num_pages = len(reader.pages)

        except Exception as e:
            print(f"❌ Failed to read PDF: {e}")
            raise e

        # Loop through pages
        for page_num in range(1, num_pages + 1):
            try:
                # Render page as image
                images = convert_from_path(
                    input_file_path, dpi=300, first_page=page_num, last_page=page_num
                )

                # OCR extraction
                text = pytesseract.image_to_string(
                    images[0],
                    lang=LANGUAGES,
                    config="--psm 6",
                )

                # Append to output text
                full_text += f"\n\n--- Page {page_num} ---\n{text}"

            except Exception as e:
                print(f"⚠️ Error on page {page_num}: {e}")

    # Save text file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"✅ Text saved to: {output_path}")

        return output_path

    except Exception as e:
        print(f"❌ Could not save file: {e}")
        raise e
