## 👁️ AI Lens — Document & Image Q&A

AI Lens is an AI-powered application that lets you upload documents or images and ask questions about them.
It combines OCR, computer vision, and LLM-based reasoning into a simple interactive interface.

---

## 🚀 Features

- 📄 Upload documents (PDF, DOCX, TXT)
- 🖼️ Upload images (JPG, PNG)
- 🔍 OCR extraction using Tesseract
- 👁️ Image understanding (YOLO + Gemini)
- 🧠 Lightweight RAG-based question answering
- 💡 Auto-generated suggested questions
- 🔄 Refresh suggestions anytime
- 💬 Interactive Q&A via Streamlit UI

---

## 🏗️ Tech Stack

# Frontend

- Streamlit

# Backend Services

- FastAPI-style modular services (no separate server required)

## AI & ML

- pytesseract (OCR)
- ultralytics YOLOv8 (object detection)
- Gemini (image description & QA)
- Groq (suggestions generation)

# Language

- Python

---

## 📁 Project Structure

AI_Lens/
│
├── frontend/
│   └── streamlit_app.py
│
├── backend/
│   └── services/
│       ├── ocr_service.py
│       ├── vision_service.py
│       ├── qa_service.py
│       ├── suggestions_service.py
│       └── storage_service.py
│
├── .env
└── requirements.txt

---

## ⚙️ Setup Instructions

1. Clone the repository

git clone <your-repo-url>
cd AI_Lens

---

2. Create virtual environment

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

---

3. Install dependencies

pip install -r requirements.txt

---

4. Add environment variables

Create a ".env" file in the root:

GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

---

5. Run the app

streamlit run frontend/streamlit_app.py

---

## 🧠 How It Works

# 📄 Document Flow

1. Upload document
2. Extract text (OCR / parser)
3. Store with "document_id"
4. Generate suggestions
5. Ask questions → RAG-based answer

---

# 🖼️ Image Flow

1. Upload image
2. OCR → extract text
3. YOLO → detect objects
4. Gemini → describe image
5. Merge into clean context
6. Store and query via Q&A

---

# 💡 Suggested Questions

- Generated using Groq (LLaMA models)
- Helps users explore content quickly
- Click to auto-fill input field
- Refresh button for new suggestions

---

# 🧪 Example Use Cases

- 📊 Analyze reports and PDFs
- 🧾 Extract info from receipts
- 🖼️ Understand images + text together
- 📚 Ask questions about study material

---

# ⚠️ Known Limitations

- OCR may be noisy for low-quality images
- Object detection may return no detections
- RAG is lightweight (not embedding-based yet)

---

# 🔮 Future Improvements

- Better RAG (embeddings)
- Chat-style UI
- Multi-document support
- API-based backend (FastAPI server)
- History tracking

---

# 🙌 Acknowledgements

- Streamlit
- Ultralytics YOLO
- Google Gemini
- Groq

---

## 👨‍💻 Author

Built by Sneh Chavan 🚀
Exploring AI, creativity, and intelligent systems.
