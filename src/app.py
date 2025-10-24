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




# Ensure session state keys are initialized





# Sidebar navigation as clickable markdown links styled as a menu (Projects only)
main_pages = ["Projects"]
if "sidebar_selection" not in st.session_state:
    st.session_state["sidebar_selection"] = "Projects"
sidebar_selection = st.session_state["sidebar_selection"]
sidebar_menu = "<h4 style='margin-bottom: 1rem;'>Navigate</h4>"
for page in main_pages:
    active_style = "background-color: #e3e8f0; color: #003366; border-radius: 6px; padding: 10px 12px; font-size: 1.15rem; font-weight: 700;" if sidebar_selection == page else "padding: 10px 12px; color: #003366; border-radius: 6px; font-size: 1.12rem; font-weight: 600;"
    sidebar_menu += f"<div style='{active_style}'><a href='#{page.replace(' ', '-')}' style='text-decoration:none;color:inherit;'>{page}</a></div>"
st.sidebar.markdown(sidebar_menu, unsafe_allow_html=True)

# Handle navigation by hash (simulate page switch)
import streamlit.components.v1 as components
nav_hash = st.experimental_get_query_params().get("nav", [sidebar_selection])[0]
if nav_hash.replace('-', ' ') in main_pages and nav_hash.replace('-', ' ') != sidebar_selection:
    st.session_state["sidebar_selection"] = nav_hash.replace('-', ' ')
    sidebar_selection = st.session_state["sidebar_selection"]

# Show recent projects in sidebar if Projects selected

# Ensure session state keys before sidebar usage
if "projects" not in st.session_state:
    st.session_state["projects"] = {}
if "current_project" not in st.session_state:
    st.session_state["current_project"] = None

recent_projects = list(st.session_state["projects"].keys())[-10:][::-1]
selected_project = None
if sidebar_selection == "Projects":
    st.sidebar.subheader("Recent Projects")
    for proj in recent_projects:
        if st.sidebar.button(proj, key=f"sidebar_proj_{proj}"):
            st.session_state["current_project"] = proj
            selected_project = proj
    if st.sidebar.button("New Project", key="sidebar_new_proj"):
        st.session_state["current_project"] = None
        st.session_state["sidebar_selection"] = "New Project"

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

if sidebar_selection == "Projects":
    st.title("Projects")
    st.markdown("Select a recent project from the sidebar to view its study tools.")
    if st.session_state.get("current_project"):
        selected = st.session_state["current_project"]
        st.write(f"**Selected Project:** {selected}")
        project = st.session_state["projects"][selected]
        tabs = st.tabs(["Flashcards", "Quiz", "Analytics"])
        with tabs[0]:
            st.subheader("Flashcards")
            for card in project.get("flashcards", []):
                st.markdown(f"**Q:** {card['question']}  \n**A:** {card['answer']}")
        with tabs[1]:
            st.subheader("Quiz")
            st.info("Quiz feature coming soon!")
        with tabs[2]:
            st.subheader("Analytics")
            st.info("Analytics feature coming soon!")
        st.write("**Notes:**")
        st.text_area("Notes", project.get("notes", ""), height=150)
    else:
        st.info("No project selected. Choose one from the sidebar.")

elif sidebar_selection == "New Project":
    st.title("Create a New Project")
    st.markdown("Enter a name for your new project.")
    new_name = st.text_input("Project name", "")
    if st.button("Add Project") and new_name:
        if new_name not in st.session_state["projects"]:
            st.session_state["projects"][new_name] = {"notes": "", "flashcards": []}
            st.success(f"Project '{new_name}' created!")
            st.session_state["current_project"] = new_name
            st.session_state["sidebar_selection"] = "Projects"
            st.rerun()
        else:
            st.warning("Project name already exists.")


