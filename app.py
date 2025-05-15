import streamlit as st
import requests
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# PDF Extractor
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# App UI
st.set_page_config(page_title="Chatbot using Groq", page_icon="🧠")
st.markdown("<h1 style='text-align: center;'>🤖 Groq Chatbot by Parth</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# PDF Upload Sidebar
st.sidebar.header("📎 Upload a PDF to Chat With It")
uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type="pdf")

pdf_text = ""
if uploaded_pdf:
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.sidebar.success("✅ PDF uploaded successfully!")
    # Store as a system message (or replace later)
    if not any(msg["role"] == "system" for msg in st.session_state.messages):
        st.session_state.messages.insert(0, {
            "role": "system",
            "content": f"Use this PDF content to answer queries:\n\n{pdf_text[:3000]}"
        })

# Display Chat Messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align: right; background-color: #dcf8c6; padding: 10px 15px; margin: 10px 0; border-radius: 12px; max-width: 80%; margin-left: auto;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    elif msg["role"] == "assistant":
        st.markdown(
            f"<div style='text-align: left; background-color: #f1f0f0; padding: 10px 15px; margin: 10px 0; border-radius: 12px; max-width: 80%; margin-right: auto;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# Chat Input
prompt = st.chat_input("Ask me anything!")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Prepare API call
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama3-8b-8192",
        "messages": st.session_state.messages
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body,
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)
    else:
        st.code(response.text, language="json")
