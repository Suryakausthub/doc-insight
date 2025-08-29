import os, json, shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()  # loads server/.env into os.environ
from dotenv import load_dotenv
load_dotenv()

from db import Base, engine, SessionLocal
from models import Upload
from schemas import Insight, HistoryItem
from services.pdf_text import extract_pdf_text
from services.freq import top5_words
from services.summarize import summarize_with_sarvam


UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Document Insight Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-resume", response_model=Insight)
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF accepted")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_pdf_text(file_path)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text in PDF")

    # Try Sarvam → fallback to freq
    summary_type = "ai"
    try:
        summary = await summarize_with_sarvam(text)
        if not summary.strip():
            raise RuntimeError("Empty AI summary")
        top_words = None
    except Exception:
        summary_type = "fallback"
        summary = None
        top_words = top5_words(text)

    # Persist
    with SessionLocal() as db:
        rec = Upload(filename=file.filename,
                     text_chars=str(len(text)),
                     summary_type=summary_type,
                     summary=summary,
                     top_words_json=json.dumps(top_words) if top_words else None)
        db.add(rec); db.commit(); db.refresh(rec)
        return Insight(
            id=rec.id,
            filename=rec.filename,
            summary_type=rec.summary_type,
            summary=rec.summary,
            top_words=json.loads(rec.top_words_json) if rec.top_words_json else None,
        )

@app.get("/insights", response_model=Insight)
def insights(id: str = Query(...)):
    with SessionLocal() as db:
        rec = db.get(Upload, id)
        if not rec:
            raise HTTPException(status_code=404, detail="Not found")
        return Insight(
            id=rec.id,
            filename=rec.filename,
            summary_type=rec.summary_type,
            summary=rec.summary,
            top_words=json.loads(rec.top_words_json) if rec.top_words_json else None,
        )

@app.get("/history", response_model=list[HistoryItem])
def history():
    with SessionLocal() as db:
        q = db.query(Upload).order_by(Upload.uploaded_at.desc()).all()
        return [HistoryItem(
            id=r.id, filename=r.filename,
            uploaded_at=r.uploaded_at.isoformat(),
            summary_type=r.summary_type
        ) for r in q]
