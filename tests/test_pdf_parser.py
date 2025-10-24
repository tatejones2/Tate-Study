import pytest
from src.pdf_parser import extract_text_from_pdf
import os

def test_extract_text_from_pdf(tmp_path):
    # Create a simple PDF for testing
    test_pdf_path = tmp_path / "test.pdf"
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hello, PDF!", ln=True)
    pdf.output(str(test_pdf_path))

    # Test extraction
    text = extract_text_from_pdf(str(test_pdf_path))
    assert "Hello, PDF!" in text
