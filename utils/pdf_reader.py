# utils/pdf_reader.py

import fitz  # PyMuPDF
from langdetect import detect

def extract_text_from_pdf(uploaded_file):
    """
    Extracts and returns full text from an uploaded PDF file.
    """
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def detect_language(text, sample_size=500):
    """
    Detects the language of a given text (first 500 characters).
    """
    try:
        return detect(text[:sample_size])
    except Exception:
        return "unknown"
