from dotenv import load_dotenv
load_dotenv()

import json
import os
from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"
def analyze_resume(resume_text: str, job_description: str):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception(
            "GROQ_API_KEY is not configured. Please add it to your .env file."
        )

    client = Groq(api_key=api_key)

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
- improvement_suggestions should contain practical suggestions for improving the resume.
- Extract candidate information from the resume when available.
- Return only JSON.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional resume analyzer. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        result = response.choices[0].message.content

        return json.loads(result)

    except json.JSONDecodeError:
        raise Exception(
            "AI returned an invalid JSON response."
        )

       

    except Exception as e:
        print("GROQ ERROR:", repr(e))
        raise Exception(
            f"Groq AI analysis failed: {str(e)}"
        )