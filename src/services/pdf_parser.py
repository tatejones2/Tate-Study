import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file using pdfplumber. Returns error message if parsing fails."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        if not text:
            return "No extractable text found in PDF."
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"
