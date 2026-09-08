import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import analyze_resume


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = extract_text_from_pdf(file_path)

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF."
            )

        return {
            "filename": file.filename,
            "text": text
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


class JobDescription(BaseModel):
    job_description: str


@router.post("/job-description")
async def add_job_description(data: JobDescription):

    if not data.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    return {
        "message": "Job description received successfully.",
        "job_description": data.job_description.strip()
    }


class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/analyze")
async def analyze_resume_api(data: ResumeAnalysisRequest):

    if not data.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty."
        )

    if not data.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    try:
        result = analyze_resume(
            data.resume_text,
            data.job_description
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )