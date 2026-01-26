import streamlit as st
import os
import pytesseract
from PIL import Image
import pdfplumber
from docx import Document

# 2026 Modular LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# --- THE KEY BYPASS ---
# Use .split() and .join() to ensure no hidden characters ruin the key
raw_key = "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"
os.environ["OPENROUTER_API_KEY"] = "".join(raw_key.split())

# 1. Page Config
st.set_page_config(page_title="Gemini Multi-Tool 2026", page_icon="🛡️")
st.title("🛡️ Resilient AI Assistant")
st.caption("OCR + Memory + 3-Model Fallback Protection")

# 2. Setup the AI Engine (With Fallback Logic)
# We use a primary model and 2 backups to handle individual model outages.
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-exp:free", 
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    extra_body={
        "models": [
            "google/gemini-2.0-flash-exp:free",      # Priority 1
            "meta-llama/llama-3.1-8b-instruct:free",   # Priority 2
            "mistralai/mistral-7b-instruct:free"     # Priority 3 (Limit of 3 reached)
        ],
        "route": "fallback"
    }
)

# 3. Session State (Memory)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_context" not in st.session_state:
    st.session_state.doc_context = ""

# 4. Extraction Logic (PDF, DOCX, and OCR for Images)
def get_file_content(uploaded_file):
    text = ""
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            img = Image.open(uploaded_file)
            text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        st.error(f"Error during extraction: {e}")
        return ""

# 5. Sidebar - Controls & Debug
with st.sidebar:
    st.header("📂 Data Source")
    uploaded_file = st.file_uploader("Upload Image/PDF/Word", type=["pdf", "docx", "png", "jpg", "jpeg"])
    
    if uploaded_file and st.button("🔄 Process File"):
        with st.spinner("Reading document..."):
            extracted = get_file_content(uploaded_file)
            if extracted:
                st.session_state.doc_context = extracted
                st.success("Context stored in memory!")
            else:
                st.warning("Could not find any text.")

    st.divider()
    if st.button("🗑️ Clear Memory"):
        st.session_state.chat_history = []
        st.session_state.doc_context = ""
        st.rerun()

    # Visual proof of what the AI is reading
    if st.session_state.doc_context:
        with st.expander("🔎 OCR/Text Output"):
            st.text(st.session_state.doc_context)

# 6. Chat Interaction
# Display history
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new input
if prompt := st.chat_input("Ask about the warranty..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Provide context to the AI model
    context = st.session_state.doc_context if st.session_state.doc_context else "No context uploaded."
    messages = [
        SystemMessage(content=f"You are a helpful assistant. Reference this text: {context}"),
        HumanMessage(content=prompt)
    ]

    with st.chat_message("assistant"):
        with st.spinner("Calling AI (using fallback if needed)..."):
            try:
                response = llm.invoke(messages)
                st.write(response.content)
                st.session_state.chat_history.append({"role": "assistant", "content": response.content})
            except Exception as e:
                # If all 3 models in the fallback fail or the global quota is hit
                st.error(f"System Error: {e}")