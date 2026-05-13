import pytesseract
from PIL import Image
import io
from config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def process_all_images(image_parts):
    combined_ocr_text = ""
    for part in image_parts:
        try:
            filename = part.get_filename() or "inline-image"
            image_data = part.get_payload(decode=True)
            img = Image.open(io.BytesIO(image_data))

            extracted = pytesseract.image_to_string(img).strip()
            if extracted:
                combined_ocr_text += f"\n--- OCR from {filename} ---\n{extracted}\n"
        except Exception as e:
            print(f"OCR failed for a part: {e}")

    return combined_ocr_text