# 📄 AI Document Insight Tool

AI Document Insight Tool is a **FastAPI + React** application that allows users to **upload PDF resumes** and receive **concise AI-generated summaries**.  
If the AI service (Sarvam AI) is unavailable, the app falls back to extracting the **top 5 most frequent words** from the PDF.

---

## ✨ Features

- Upload **PDF resumes** only (validated in backend).  
- **AI-powered summary** using [Sarvam AI](https://sarvam.ai).  
- **Fallback mode**: top 5 frequent words from PDF if AI fails.  
- **History tab**: view all past uploads.  
- **Insights endpoint**: retrieve summary for a specific file.  
- Fully **containerized with Docker Compose** for seamless deployment.  

---

## 📂 Project Structure
```
doc-insight/
├─ server/ # FastAPI backend
│ ├─ app.py # Main application
│ ├─ db.py, models.py, schemas.py
│ ├─ services/
│ │ ├─ pdf_text.py # PDF text extraction
│ │ ├─ summarize.py # Sarvam AI client
│ │ └─ freq.py # Top-5 words fallback
│ ├─ uploads/ # Persisted PDF uploads
│ ├─ requirements.txt
│ ├─ Dockerfile
│ └─ .env.example # Copy as .env and add secrets
├─ web/ # React frontend
│ ├─ src/
│ │ ├─ api.ts # Axios client
│ │ ├─ components/ # Uploader, InsightCard, HistoryList
│ │ └─ pages/ # Upload, History
│ ├─ Dockerfile
├─ docker-compose.yml
├─ .gitignore
└─ README.md
```

---

## ⚙️ Backend Setup (Local)

```
cd server
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Copy environment file
copy .env.example .env
# Add your Sarvam AI API key in .env

# Run backend
python -m uvicorn app:app --reload
# API docs → http://127.0.0.1:8000/docs

```
---

## 💻 Frontend Setup (Local)
```
cd web
npm install
```
## Set backend URL during local dev
```
echo VITE_API_URL=http://127.0.0.1:8000 > .env

npm run dev
```
## Frontend → http://localhost:5173

---
## 🐳 Docker Setup (Recommended)

From the project root:
```
docker compose build
docker compose up -d
```
```
Frontend → http://localhost:5173
Backend → http://localhost:8000/docs
```
To rebuild frontend (after code/env changes):
```
docker compose build web --no-cache
docker compose up -d
```

## 📡 API Endpoints
1. POST /upload-resume
Upload a PDF file.
Response (AI success):
```
{
  "id": "uuid",
  "filename": "resume.pdf",
  "summary_type": "ai",
  "summary": "Concise AI summary text",
  "top_words": null
}
```
Response (AI fails):
```
{
  "id": "uuid",
  "filename": "resume.pdf",
  "summary_type": "fallback",
  "summary": null,
  "top_words": [["python", 12], ["java", 8], ...]
}
```
2. GET /history
List of previous uploads:
```
[
  {
    "id": "uuid",
    "filename": "resume.pdf",
    "uploaded_at": "2025-08-29T12:34:56",
    "summary_type": "ai"
  }
]
```
3. GET /insights?id=<uuid>
Fetch a specific upload’s details:
```
{
  "id": "uuid",
  "filename": "resume.pdf",
  "summary_type": "ai",
  "summary": "Concise AI summary text",
  "top_words": null
}
```

## 🔑 Environment Variables
```
Backend (server/.env)
SARVAM_API_KEY=your_api_key_here
SARVAM_API_URL=https://api.sarvam.ai/v1/chat/completions
SUMMARY_MODEL=sarvam-m
MAX_PDF_SIZE_MB=10
```
```
Frontend (web/.env during local dev)
VITE_API_URL=http://127.0.0.1:8000
```

## 🚀 Future Improvements
```
OCR support for scanned PDFs.
Better visualization of summaries.
User accounts & authentication.
PostgreSQL instead of SQLite for multi-user setup.
Metrics & health-check endpoints.
```
## 📚 References
```
FastAPI Documentation
React Documentation
Sarvam AI
```
