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
    user_question,
    retrieved_context=""
):

    prompt = f"""
You are an AI Resume Assistant.

Answer the user's question using the retrieved knowledge first.
If the retrieved knowledge is not sufficient, use the resume and job description.

Rules:
1. Never invent skills or experience.
2. Use the resume as the primary source for candidate information.
3. Use the retrieved knowledge for ATS rules, interview guidance, and career advice.
4. If something is missing from the resume, clearly say so.

==============================
RETRIEVED KNOWLEDGE
==============================

{retrieved_context}

==============================
RESUME
==============================

{resume_text}

==============================
JOB DESCRIPTION
==============================

{job_description}

==============================
USER QUESTION
==============================

{user_question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text