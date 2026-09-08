from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.resume import router as resume_router


app = FastAPI(
    title="AI Resume Analyzer",
    description="Analyze resumes against job descriptions using AI",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-resume-analyzer-1-hil6.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(resume_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Resume Analyzer backend is running"
    }