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



# Multipage navigation

# Set Upload as default page
page = st.sidebar.radio(
    "Navigate",
    ("Upload & Flashcards", "Projects")
)

if "projects" not in st.session_state:
    st.session_state["projects"] = {}
if "current_project" not in st.session_state:
    st.session_state["current_project"] = None

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    st.success("OpenAI API key loaded successfully.")
else:
    st.error("OpenAI API key not found. Please check your .env file.")

from services.pdf_parser import extract_text_from_pdf
from services.flashcard_generator import generate_flashcards

if page == "Projects":
    st.title("Projects")
    st.markdown("Manage your study projects. Each project can have its own notes and flashcards.")
    project_names = list(st.session_state["projects"].keys())
    selected = st.selectbox("Select a project", ["(None)"] + project_names)
    if selected != "(None)":
        st.session_state["current_project"] = selected
        st.write(f"**Selected Project:** {selected}")
        project = st.session_state["projects"][selected]
        st.write("**Notes:**")
        st.text_area("Notes", project.get("notes", ""), height=150)
        st.write("**Flashcards:**")
        for card in project.get("flashcards", []):
            st.markdown(f"**Q:** {card['question']}  \n**A:** {card['answer']}")
    st.markdown("---")
    new_name = st.text_input("Create a new project", "")
    if st.button("Add Project") and new_name:
        if new_name not in st.session_state["projects"]:
            st.session_state["projects"][new_name] = {"notes": "", "flashcards": []}
            st.success(f"Project '{new_name}' created!")
        else:
            st.warning("Project name already exists.")

elif page == "Upload & Flashcards":
    st.title("Upload Notes & Generate Flashcards")
    st.markdown("Upload your class notes as a PDF, extract the text, and generate flashcards.")
    uploaded_file = st.file_uploader("Upload your class notes (PDF)", type=["pdf"])
    extracted_text = handle_pdf_upload(uploaded_file)
    if extracted_text is not None:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.subheader("Extracted Text from PDF:")
            st.text_area("PDF Content", extracted_text, height=300)
        with col2:
            st.subheader("Flashcards")
            if st.button("Generate Flashcards"):
                with st.spinner("Generating flashcards..."):
                    flashcards = generate_flashcards(extracted_text)
                for card in flashcards:
                    st.markdown(f"**Q:** {card['question']}  \n**A:** {card['answer']}")
                # Prompt for project name and save
                new_proj_name = st.text_input("Save this session as a new project. Enter project name:", "")
                if st.button("Save Project") and new_proj_name:
                    if new_proj_name not in st.session_state["projects"]:
                        st.session_state["projects"][new_proj_name] = {"notes": extracted_text, "flashcards": flashcards}
                        st.success(f"Project '{new_proj_name}' saved!")
                    else:
                        st.warning("Project name already exists.")
