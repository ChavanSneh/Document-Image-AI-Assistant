from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from .services.ocr_service import process_document
from .services.storage_service import save_document, get_document
from .services.qa_service import answer_question
from .services.vision_service import run_dual_pipelines

router = APIRouter()

class AskRequest(BaseModel):
    document_id: str | None = None  # optional now
    question: str

@router.post("/scan")
async def scan_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        result = process_document(file_bytes, file.filename)
        return {"filename": file.filename, "text": result["text"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        # --- IMAGE FLOW ---
        if file.content_type.startswith("image/"):
            from services.vision_service import run_dual_pipelines

            result = run_dual_pipelines(file_bytes)

            # combine everything into text for storage
            full_text = f"""
Image Type: {result.get("image_type")}
Description: {result.get("visual_description")}
Objects: {result.get("detected_objects")}
Text: {result.get("extracted_text")}
"""

            doc_id = save_document(full_text)
            preview = full_text[:500]

            return {
                "document_id": doc_id,
                "preview": preview
            }

        # --- DOCUMENT FLOW (UNCHANGED) ---
        result = process_document(file_bytes, file.filename)
        text = result["text"]
        doc_id = save_document(text)
        preview = text[:500]

        return {
            "document_id": doc_id,
            "preview": preview
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ask")
async def ask_question(payload: AskRequest):
    if payload.document_id:
        text = get_document(payload.document_id)
        if text is None:
            raise HTTPException(status_code=404, detail="Document not found")
    else:
        text = ""  # no document context

    answer = answer_question(text, payload.question)
    return {"document_id": payload.document_id, "answer": answer}