import ocrmypdf
import os
from pathlib import Path

from ocr import LANGUAGES

# Supported image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


def convert_to_ocr(input_file_path):
    """
    Converts a PDF or image file into an OCR searchable PDF.
    Returns the output file path.
    """

    # Ensure outputs folder exists
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    # Check if input is image
    file_ext = Path(input_file_path).suffix.lower()
    is_image = file_ext in IMAGE_EXTENSIONS

    # If it's an image, convert to PDF first
    if is_image:
        try:
            from PIL import Image

            print(f"📷 Converting image to PDF: {input_file_path}")

            image = Image.open(input_file_path)

            # Convert RGBA to RGB if necessary
            if image.mode == "RGBA":
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image
            elif image.mode != "RGB":
                image = image.convert("RGB")

            # Create temporary PDF from image
            base = os.path.splitext(os.path.basename(input_file_path))[0]
            temp_pdf_path = os.path.join(output_folder, f"{base}_temp.pdf")
            image.save(temp_pdf_path, "PDF")
            input_file_path = temp_pdf_path
            print(f"✅ Image converted to PDF")
        except Exception as e:
            print(f"❌ Failed to convert image to PDF: {e}")
            raise e

    # Output filename
    base = os.path.splitext(os.path.basename(input_file_path))[0]
    output_pdf_path = os.path.join(output_folder, f"{base}_ocr.pdf")

    try:
        ocrmypdf.ocr(
            input_file_path,
            output_pdf_path,
            language=LANGUAGES,
            force_ocr=True,
            deskew=True,
            rotate_pages=True,
            optimize=3,
            image_dpi=300,  # Set default DPI for images without metadata
            png_quality=85,  # Set PNG quality to avoid NoneType error
        )
        print(f"✅ OCR PDF created: {output_pdf_path}")
        return output_pdf_path

    except Exception as e:
        print(f"❌ OCR conversion failed: {e}")
        raise e
