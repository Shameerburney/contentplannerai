import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
