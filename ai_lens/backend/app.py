from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from.routes import router

app = FastAPI(
    title="AI Document Q&A Service",
    description="API to extract text from images, PDFs, DOCX, TXT, store documents, and ask questions about the content",
    version="1.0.0"
)

app.include_router(router)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/health")
async def health_check():
    return {"status": "active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)