# 🛡️ Resilient Hybrid AI Assistant (2026 Edition)

An advanced Document AI Assistant that allows users to chat with PDFs, Word Documents, and Images using the fastest AI models available today.

## 🚀 Key Features
- **Dual-Engine Switching:** Toggle between **Google Gemini 2.0** (via OpenRouter) for deep reasoning and **Groq (Llama 3.3)** for lightning-fast responses.
- **Multi-Format OCR:** Extract text from PDFs, `.docx` files, and images (PNG/JPG) using `pytesseract` and `pdfplumber`.
- **Hybrid Security:** Built-in protection for API keys using Streamlit Secrets and `.gitignore` safety protocols.
- **Smart History:** Interactive live chat interface with "Clear Memory" functionality.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **AI Orchestration:** LangChain
- **Models:** Gemini 2.0 Flash, Llama 3.3 (70B)
- **Engines:** OpenRouter & Groq Cloud
- **OCR & Parsing:** Tesseract OCR, Pdfplumber, Python-Docx

## ⚙️ Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ChavanSneh/Document-Image-AI-Assistant.git](https://github.com/ChavanSneh/Document-Image-AI-Assistant.git)
   cd Document-Image-AI-Assistant
2. **Install Depencencies:**
   pip install -r requirements.txt
3. **Configure Secrets:**
   Create a folder named .streamlit and a file named secrets .toml inside it: OPENROUTER_API_KEY = "your_openrouter_key"
   GROQ_API_KEY = "your_groq_key"
4. **Run the App:**
   streamlit run streamlit_app.py
