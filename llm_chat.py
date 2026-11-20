
import os

from dotenv import load_dotenv
from google import genai
from langsmith import traceable, get_current_run_tree

from tracing_utils import (
    safe_trace_inputs,
    safe_trace_outputs
)

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"


@traceable(
    name="Gemini Resume Assistant",
    run_type="llm",
    metadata={
        "ls_provider": "google",
        "ls_model_name": MODEL_NAME
    },
    process_inputs=safe_trace_inputs,
    process_outputs=safe_trace_outputs
)
def ask_resume_ai(
    resume_text,
    job_description,
    user_question,
    retrieved_context=""
):

    # Construct prompt
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

    # Generate response using Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    # Extract token usage from Gemini
    usage = response.usage_metadata

    if usage:
        input_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        total_tokens = usage.total_token_count or 0

        token_usage = {
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens),
            "total_tokens": int(total_tokens)
        }

        # Send token usage to LangSmith
        run = get_current_run_tree()

        if run is not None:
            run.set(usage_metadata=token_usage)

        print("Gemini Token Usage:", token_usage)

    # Return Gemini response
    return response.text

