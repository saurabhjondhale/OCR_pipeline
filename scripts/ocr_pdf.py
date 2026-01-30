import ocrmypdf
import os

LANGUAGES = "mar+hin+san+eng"

def convert_to_ocr(input_pdf_path):
    """
    Converts a single PDF into an OCR searchable PDF.
    Returns the output file path.
    """

    # Ensure outputs folder exists
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    # Output filename
    output_pdf_path = os.path.join(output_folder, os.path.basename(input_pdf_path))

    try:
        ocrmypdf.ocr(
            input_pdf_path,
            output_pdf_path,
            language=LANGUAGES,
            force_ocr=True,
            deskew=True,
            rotate_pages=True,
            optimize=3
        )
        print(f"✅ OCR PDF created: {output_pdf_path}")
        return output_pdf_path

    except Exception as e:
        print(f"❌ OCR conversion failed: {e}")
        raise e
