import os
import re
from dotenv import load_dotenv
from google  import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment")

client = genai.Client(api_key=api_key)



def _chunk_text(text: str, size: int = 800) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []

    for p in paragraphs:
        if len(p) <= size:
            chunks.append(p)
        else:
            chunks.extend([p[i:i+size] for i in range(0, len(p), size)])

    return chunks


def _pick_chunks(chunks: list[str], question: str, k: int = 3) -> list[str]:
    q_words = set(question.lower().split())
    scored = []

    for c in chunks:
        score = sum(c.lower().count(w) for w in q_words)
        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    # fallback if nothing matches
    top_chunks = [c for score, c in scored[:k] if score > 0]
    return top_chunks if top_chunks else chunks[:k]


def answer_question(document_text: str, question: str) -> str:
    chunks = _chunk_text(document_text)
    selected_chunks = _pick_chunks(chunks, question)
    context = "\n\n---\n\n".join(selected_chunks)

    prompt = f"""
You are an intelligent assistant answering questions about a document or image.

The content may include:
- Extracted text (OCR)
- Detected objects
- Image description

Use ALL available context to answer.

Context:
{context}

Question:
{question}

Rules:
- Answer clearly and concisely
- If question is about objects, use detected objects
- If question is about meaning, use description
- If question is about text, use extracted text
- If answer is not present, say:
  "I couldn't find the answer in the document."

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return (response.text or "").strip()