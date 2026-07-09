import os

from dotenv import load_dotenv
from google import genai


# Load .env file
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Check API key
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )


# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_resume_ai(
    resume_text,
    job_description,
    user_question
):

    prompt = f"""
You are an AI Resume Assistant.

Analyze the candidate's resume and job description.

Rules:
1. Answer the user's question clearly.
2. Use the resume as context.
3. Use the job description as context.
4. Do not invent skills or experience.
5. Provide practical suggestions.

RESUME:

{resume_text}


JOB DESCRIPTION:

{job_description}


USER QUESTION:

{user_question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text