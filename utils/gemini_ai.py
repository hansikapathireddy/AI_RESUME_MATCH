import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def get_ai_feedback(resume_text, job_description):

    if not API_KEY:
        return "❌ Gemini API key is not configured."


    # ========================================================
    # MODELS - AUTOMATIC FALLBACK
    # ========================================================

    models = [
        "models/gemini-3.8-flash",
        "models/gemini-3.7-flash",
        "models/gemini-3.6-flash",
        "models/gemini-3.5-flash",
        "models/gemini-3.1-flash-lite",
        "models/gemini-3-flash-preview",
        "models/gemini-2.5-flash"
    ]


    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are an expert resume and career assistant.

Analyze the following resume against the given job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Give the analysis using these sections:

## Resume Strengths

## Matching Skills

## Missing Skills

## Resume Weaknesses

## ATS Improvement Suggestions

## Recommended Projects

## Recommended Skills to Learn

## Overall Recommendation

Rules:
- Do not invent experience, skills, projects, or achievements.
- Only use information supported by the resume and job description.
- Give practical and concise suggestions.
- Focus on the target job.
"""


    # ========================================================
    # GEMINI CLIENT
    # ========================================================

    try:

        client = genai.Client(
            api_key=API_KEY
        )

    except Exception as e:

        return f"❌ Gemini client error: {type(e).__name__}: {e}"


    # ========================================================
    # TRY MODELS ONE BY ONE
    # ========================================================

    errors = []

    for model in models:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response and response.text:

                return response.text


        except Exception as e:

            error_text = str(e)

            errors.append(
                f"{model}: {error_text}"
            )

            # If model is temporarily busy, try next model
            if "503" in error_text or "UNAVAILABLE" in error_text:

                time.sleep(1)

                continue

            # For other errors also try next available model
            continue


    # ========================================================
    # ALL MODELS FAILED
    # ========================================================

    return (
        "❌ Gemini is temporarily unavailable.\n\n"
        "All configured Gemini models were busy or unavailable. "
        "Please try the AI analysis again after a short time.\n\n"
        "Your Resume Analysis, Job Match and ATS Score are still working."
    )