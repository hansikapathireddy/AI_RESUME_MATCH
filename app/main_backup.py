import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


def get_ai_feedback(resume_text, job_description):

    if not API_KEY:
        return "Gemini API key is not configured."

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        prompt = f"""
You are an expert resume and career assistant.

Analyze the following resume against the given job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide a concise but useful analysis with these sections:

1. Resume Strengths
2. Missing Skills
3. Resume Weaknesses
4. ATS Improvement Suggestions
5. Recommended Projects
6. Recommended Skills to Learn
7. Overall Recommendation

Do not invent experience or skills that are not present in the resume.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini AI Error: {e}"