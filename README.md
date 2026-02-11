
🛡️ Resilient Hybrid AI Assistant (2026 Edition)
This project was originally built as a real-world experiment.
For this challenge, I’m submitting an existing, fully working solution rather than rebuilding from scratch.
The goal was to design a fast, resilient, and practical Document AI system, not a toy demo.

🔍 Overview
An advanced Document AI Assistant that enables users to chat with PDFs, Word documents, and images, leveraging modern LLMs and OCR pipelines.
The system is designed to balance reasoning depth, response speed, and reliability by dynamically switching between AI engines.

🚀 Key Features
Dual-Engine AI Switching
Switch between Google Gemini 2.0 (via OpenRouter) for deep reasoning and Groq (Llama 3.3) for ultra-fast responses.
Multi-Format Document Support
Extracts and processes text from:
PDFs
.docx files
Images (PNG, JPG) using OCR
Hybrid Security Design
API keys are protected using Streamlit Secrets and .gitignore safety practices.
Interactive Chat Interface
Live conversational UI with session memory and Clear Memory controls.

🛠️ Tech Stack
Frontend: Streamlit
AI Orchestration: LangChain
Models: Gemini 2.0 Flash, Llama 3.3 (70B)
Inference Providers: OpenRouter, Groq Cloud
OCR & Parsing: Tesseract OCR, PdfPlumber, Python-Docx

⚙️ Local Setup

Clone the Repository

git clone https://github.com/ChavanSneh/Document-Image-AI-Assistant.git
cd Document-Image-AI-Assistant

Install Dependencies

pip install -r requirements.txt

Configure Secrets

Create a .streamlit folder and add a secrets.toml file:

Toml

OPENROUTER_API_KEY = "your_openrouter_key"
GROQ_API_KEY = "your_groq_key"

Run the App

streamlit run streamlit_app.py 