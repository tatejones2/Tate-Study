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
from config.style_config import STYLE


load_dotenv()

# Inject custom CSS for sitewide styles
st.markdown(f"""
    <style>
        body, .stApp {{
            background-color: {STYLE['background_color']};
            color: {STYLE['text_color']};
            font-family: {STYLE['body_font']};
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: {STYLE['header_font']};
            color: {STYLE['primary_color']};
        }}
        .stTextArea textarea {{
            background-color: {STYLE['secondary_color']};
            color: {STYLE['primary_color']}; /* Navy text for contrast */
            font-size: 1rem;
        }}
        .stButton>button {{
            background-color: {STYLE['primary_color']};
            color: #fff;
            font-weight: bold;
        }}
        .stMarkdown, .stSubheader {{
            color: {STYLE['text_color']};
        }}
    </style>
""", unsafe_allow_html=True)

st.title("TateStudy")
st.write("Welcome to your AI-powered study tool!")

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    st.success("OpenAI API key loaded successfully.")
else:
    st.error("OpenAI API key not found. Please check your .env file.")

from services.pdf_parser import extract_text_from_pdf
from services.flashcard_generator import generate_flashcards

# PDF upload and extraction

uploaded_file = st.file_uploader("Upload your class notes (PDF)", type=["pdf"])
extracted_text = handle_pdf_upload(uploaded_file)
if extracted_text is not None:
    st.subheader("Extracted Text from PDF:")
    st.text_area("PDF Content", extracted_text, height=300)

    # Generate flashcards from extracted text
    if st.button("Generate Flashcards"):
        with st.spinner("Generating flashcards..."):
            flashcards = generate_flashcards(extracted_text)
        st.subheader("Generated Flashcards:")
        for card in flashcards:
            st.markdown(f"**Q:** {card['question']}  \n**A:** {card['answer']}")
