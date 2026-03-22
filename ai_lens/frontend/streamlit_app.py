import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.services.ocr_service import process_document
from backend.services.storage_service import save_document, get_document
from backend.services.qa_service import answer_question
from backend.services.vision_service import run_dual_pipelines
from backend.services.suggestions_service import generate_suggestions

st.set_page_config(page_title="AI Lens", page_icon="👁️")

st.title("👁️ AI Lens - Document & Image Q&A")

uploaded_file = st.file_uploader(
    "Upload image, PDF, DOCX or TXT",
    type=["png", "jpg", "jpeg", "pdf", "docx", "txt"]
)

# --- Upload Handling ---
if uploaded_file:
    file_bytes = uploaded_file.read()

    # We only process if doc_id isn't already in session state (prevents re-running on every click)
    if "doc_id" not in st.session_state:
        # IMAGE FLOW
        if uploaded_file.type.startswith("image/"):
            result = run_dual_pipelines(file_bytes)
            description = result.get("visual_description") or ""
            ocr_text = result.get("extracted_text") or ""
            
            if len(ocr_text.strip()) < 20:
                ocr_text = ""

            full_text = f"{description}\n\n{ocr_text}"
            doc_id = save_document(full_text)
            st.session_state.doc_id = doc_id
            st.success("Image processed")
        
        # DOCUMENT FLOW
        else:
            result = process_document(file_bytes, uploaded_file.name)
            doc_id = save_document(result["text"])
            st.session_state.doc_id = doc_id
            st.success("Document processed")

    # --- Suggestions ---
    # Fetch text once doc_id is available
    text = get_document(st.session_state.doc_id)

    if "suggestions" not in st.session_state:
        st.session_state.suggestions = generate_suggestions(text)

    st.divider()
    col1, col2 = st.columns([4, 1])

    with col1:
        st.subheader("💡 Suggested Questions")

    with col2:
        if st.button("🔄"):
            st.session_state.suggestions = generate_suggestions(text)
            st.rerun()

    # Indented loop to avoid NameError
    suggestions = st.session_state.get("suggestions", [])
    for q in suggestions:
        if st.button(q):
            st.session_state.user_question = q  # Fills the text bar
            st.rerun()

    # --- Ask Section ---
    st.divider()
    st.subheader("💬 Ask a Question")

    # Linked to st.session_state.user_question
    user_q = st.text_input("Type your question here", key="user_question")

    if st.button("Ask"):
        if user_q:
            doc_id = st.session_state.get("doc_id")
            current_text = get_document(doc_id) if doc_id else ""

            with st.spinner("Thinking..."):
                ans = answer_question(current_text, user_q)
                st.session_state.answer = ans
        else:
            st.warning("Please enter a question or click a suggestion first.")

    # Display answer
    if "answer" in st.session_state and st.session_state.answer:
        st.subheader("🤖 Bot Answer")
        st.text_area(
            label="Response", 
            value=st.session_state.answer, 
            height=200, 
            disabled=True
        )
else:
    # Optional: Clear state if file is removed
    st.info("Please upload a file to begin.")
    st.session_state.clear()