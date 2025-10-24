# Helper function for PDF upload and extraction
def handle_pdf_upload(uploaded_file):
    if uploaded_file is not None:
        temp_path = "temp_uploaded.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        from services.pdf_parser import extract_text_from_pdf
        extracted_text = extract_text_from_pdf(temp_path)
        return extracted_text
    return None
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.title("TateStudy")
st.write("Welcome to your AI-powered study tool!")

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    st.success("OpenAI API key loaded successfully.")
else:
    st.error("OpenAI API key not found. Please check your .env file.")

from services.pdf_parser import extract_text_from_pdf

# PDF upload and extraction

uploaded_file = st.file_uploader("Upload your class notes (PDF)", type=["pdf"])
extracted_text = handle_pdf_upload(uploaded_file)
if extracted_text is not None:
    st.subheader("Extracted Text from PDF:")
    st.text_area("PDF Content", extracted_text, height=300)
