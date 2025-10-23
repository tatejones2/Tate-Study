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
