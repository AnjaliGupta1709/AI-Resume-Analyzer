# AI Resume Analyzer

AI Resume Analyzer is a web-based application that analyzes a candidate's resume against a given job description using a local AI model.

The application extracts information from a PDF resume and compares it with the job description to provide a match score, matching skills, missing skills, and improvement suggestions.

## Features

- Upload resume in PDF format
- Extract text from PDF resume
- Enter a job description
- Analyze resume against the job description
- Generate an AI-based match score
- Extract candidate information
  - Name
  - Email
  - Phone
  - Location
- Identify matching skills
- Identify missing skills
- Generate resume improvement suggestions
- Local AI processing using Ollama
- Swagger/OpenAPI documentation
- Health check endpoint
- React-based frontend
- FastAPI backend

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- Requests

### AI

- Ollama
- Llama 3.2 1B

## Project Structure

```text
ai-resume-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── resume.py
│   │   │
│   │   └── services/
│   │       ├── ai_service.py
│   │       └── pdf_service.py
│   │
│   ├── uploads/
│   ├── main.py
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   │
│   └── ...
│
└── README.md