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

from pdf_parser import extract_text_from_pdf

# PDF upload and extraction
uploaded_file = st.file_uploader("Upload your class notes (PDF)", type=["pdf"])
if uploaded_file is not None:
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    extracted_text = extract_text_from_pdf("temp_uploaded.pdf")
    st.subheader("Extracted Text from PDF:")
    st.text_area("PDF Content", extracted_text, height=300)
