import os
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

LANGS = "eng+san+hin+malayalam+telugu+gujarati+punjabi+marathi+bengali+odia+tamil+kannada"

def extract_text(input_pdf_path):
    """
    Extracts OCR text from a PDF and saves as .txt
    Returns the path to the text file.
    """

    # Make output folder
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    # Get output filename
    base = os.path.splitext(os.path.basename(input_pdf_path))[0]
    output_path = os.path.join(output_folder, f"{base}_extracted.txt")

    # Try reading number of pages
    try:
        reader = PdfReader(input_pdf_path)
        num_pages = len(reader.pages)
    except Exception as e:
        print(f"❌ Failed to read PDF: {e}")
        raise e

    full_text = ""

    # Loop through pages
    for page_num in range(1, num_pages + 1):
        try:
            # Render page as image
            images = convert_from_path(input_pdf_path, dpi=300, first_page=page_num, last_page=page_num)

            # OCR extraction
            text = pytesseract.image_to_string(images[0], lang=LANGS, config="--psm 6")

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
