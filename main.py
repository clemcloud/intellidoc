import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from extraction import extract_text
from analysis import analyze_with_gemini
from database import SessionLocal, Document, init_db

app = FastAPI(title="IntelliDoc")

# frontend is served straight from FastAPI now, so allow it to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# make sure the table exists before we start taking requests
init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    saved_name = f"{uuid.uuid4()}{ext}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)

    with open(saved_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    db = SessionLocal()

    # create the row first so we have something to point to even if processing fails
    doc = Document(filename=file.filename, status="pending")
    db.add(doc)
    db.commit()
    db.refresh(doc)

    try:
        text = extract_text(saved_path)
        result = analyze_with_gemini(text)
    except ValueError as e:
        doc.status = "failed"
        doc.result = {"error": str(e)}
        db.commit()
        db.close()
        raise HTTPException(status_code=400, detail=str(e))

    doc.status = "done"
    doc.result = result
    db.commit()

    # grab the values we need before closing the session, otherwise
    # sqlalchemy can't touch the object anymore (DetachedInstanceError)
    response_data = {
        "id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "result": doc.result,
    }
    db.close()

    return response_data


@app.get("/documents/{document_id}")
def get_document(document_id: str):
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == document_id).first()

    if not doc:
        db.close()
        raise HTTPException(status_code=404, detail="document not found")

    response_data = {
        "id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "result": doc.result,
    }
    db.close()

    return response_data


@app.get("/health")
def health():
    return {"status": "ok"}