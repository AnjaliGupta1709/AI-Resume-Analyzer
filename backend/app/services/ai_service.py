import json
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"


def analyze_resume(resume_text: str, job_description: str):

    prompt = f"""
You are an AI Resume Analyzer.

Analyze the candidate's resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON in this exact structure:

{{
    "candidate_information": {{
        "name": "",
        "email": "",
        "phone": "",
        "location": ""
    }},
    "matching_skills": [],
    "missing_skills": [],
    "match_score": 0,
    "improvement_suggestions": []
}}

Rules:
- match_score must be a number from 0 to 100.
- matching_skills must contain skills present in both the resume and job description.
- missing_skills must contain important skills from the job description that are missing from the resume.
- improvement_suggestions must contain practical suggestions.
- Extract candidate information from the resume.
- Return only JSON.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional resume analyzer. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "format": "json",
                "keep_alive": "10m",
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        result = data["message"]["content"]

        return json.loads(result)

    except requests.exceptions.ConnectionError:
        raise Exception(
            "Ollama is not running. Please start Ollama and try again."
        )

    except requests.exceptions.Timeout:
        raise Exception(
            "AI analysis timed out. Please try again."
        )

    except json.JSONDecodeError:
        raise Exception(
            "AI returned an invalid JSON response."
        )

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Ollama request failed: {str(e)}"
        )