import streamlit as st
import os

# --- 1. SECURITY & API CONFIG ---
# This looks for BOTH keys in your .streamlit/secrets.toml
if "OPENROUTER_API_KEY" in st.secrets and "GROQ_API_KEY" in st.secrets:
    os.environ["OPENROUTER_API_KEY"] = st.secrets["OPENROUTER_API_KEY"]
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    st.error("🔑 API Keys not found! Ensure BOTH 'OPENROUTER_API_KEY' and 'GROQ_API_KEY' are in your secrets.toml.")
    st.stop()

# --- 2. IMPORTS (Correctly Aligned to Left Wall) ---
import pytesseract
from PIL import Image
import pdfplumber
from docx import Document
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# --- 3. PAGE CONFIGURATION ---
st.set_page_config(page_title="Resilient Hybrid AI", page_icon="⚡", layout="wide")
st.title("⚡ Resilient Hybrid AI Assistant")
st.markdown("OCR + PDF Analysis | Gemini (Stable) & Groq (Lightning Fast)")

# --- 4. INITIALIZE SESSION STATES ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

# --- 5. SIDEBAR: SETTINGS & UPLOADS ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    # Toggle between your direct Groq key and the OpenRouter fallback
    engine_choice = st.radio(
        "Select AI Engine:",
        ("Gemini (via OpenRouter)", "Groq (Direct Speed)"),
        index=1
    )

    st.divider()
    st.header("📁 Document Upload")
    uploaded_file = st.file_uploader("Upload Image, PDF, or Word", type=["pdf", "docx", "png", "jpg", "jpeg"])
    
    if st.button("Process Document ⚙️"):
        if uploaded_file:
            with st.spinner("Extracting content..."):
                text = ""
                if uploaded_file.type == "application/pdf":
                    with pdfplumber.open(uploaded_file) as pdf:
                        text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = Document(uploaded_file)
                    text = "\n".join([para.text for para in doc.paragraphs])
                elif "image" in uploaded_file.type:
                    img = Image.open(uploaded_file)
                    text = pytesseract.image_to_string(img)
                
                st.session_state.extracted_text = text
                st.success("Analysis Complete!")
        else:
            st.warning("Please upload a file first.")

    if st.button("Clear History 🧹"):
        st.session_state.messages = []
        st.session_state.extracted_text = ""
        st.rerun()

# --- 6. DYNAMIC ENGINE LOADING ---
if engine_choice == "Groq (Direct Speed)":
    # Using your direct Groq API Key
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        groq_api_key=st.secrets["GROQ_API_KEY"]
    )
else:
    # Using OpenRouter (Gemini) with fallbacks
    llm = ChatOpenAI(
        model="google/gemini-2.0-flash-exp:free",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1"
    )

# --- 7. LIVE CHAT INTERFACE ---
# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Combine context with user query
        context_data = st.session_state.extracted_text if st.session_state.extracted_text else "No document data provided."
        full_query = f"DOCUMENT DATA:\n{context_data}\n\nUSER QUESTION: {prompt}"
        
        try:
            st.caption(f"🧠 Processor: {engine_choice}")
            response = llm.invoke([HumanMessage(content=full_query)])
            st.markdown(response.content)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
        except Exception as e:
            st.error(f"Engine Error: {str(e)}")