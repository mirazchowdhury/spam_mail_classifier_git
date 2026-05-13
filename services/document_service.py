# services/document_service.py
import io
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_content):
    """PDF file theke text extract kora"""
    try:
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"[PDF Extraction Error: {e}]"


def extract_text_from_docx(file_content):
    """DOCX file theke text extract kora"""
    try:
        docx_file = io.BytesIO(file_content)
        doc = Document(docx_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"[DOCX Extraction Error: {e}]"


def process_all_attachments(doc_parts):
    """Shob attachment check kore text ber kora"""
    combined_doc_text = ""
    for part in doc_parts:
        filename = part.get_filename() or "unknown_file"
        content = part.get_payload(decode=True)

        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(content)
            combined_doc_text += f"\n--- Content from PDF: {filename} ---\n{text}\n"
        elif filename.lower().endswith((".docx", ".doc")):
            text = extract_text_from_docx(content)
            combined_doc_text += f"\n--- Content from DOC: {filename} ---\n{text}\n"

    return combined_doc_text