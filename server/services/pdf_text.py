from io import BytesIO
from pdfminer.high_level import extract_text

def extract_pdf_text(file_path: str) -> str:
    return extract_text(file_path) or ""
