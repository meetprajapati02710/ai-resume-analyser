import time
from llm_chat import ask_resume_ai


def generate_interview_questions(
    resume_text,
    job_description,
    num_questions=10,
    interview_mode="Standard Interview"
):
    """
    Generate AI interview questions based on the
    candidate's resume and job description.
    """

    if interview_mode == "Quick Interview":
        difficulty = "Easy"

    elif interview_mode == "Standard Interview":
        difficulty = "Medium"

    elif interview_mode == "Comprehensive Interview":
        difficulty = "Hard"

    else:
        difficulty = "Expert"

    prompt = f"""
You are a Senior Technical Interviewer at a top technology company.

Generate exactly {num_questions} interview questions.

Candidate Resume:
{resume_text}

Job Description:
{job_description}

Interview Mode:
{interview_mode}

Difficulty:
{difficulty}

Instructions:

1. Generate exactly {num_questions} questions.

2. Number every question.

3. Do NOT provide answers.

4. Mix these categories:

- Resume-based
- Project-based
- Technical
- Coding
- Scenario-based
- Behavioral

5. Questions should gradually increase in difficulty.

6. Focus on the candidate's projects.

7. Return ONLY the questions.
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:

            return ask_resume_ai(
                resume_text=resume_text,
                job_description=job_description,
                user_question=prompt,
                retrieved_context=""
            )

        except Exception as e:

            error = str(e)

            if (
                "503" in error
                or "UNAVAILABLE" in error
                or "429" in error
                or "RESOURCE_EXHAUSTED" in error
            ):

                if attempt < max_retries - 1:
                    time.sleep(5 * (attempt + 1))
                    continue

                return (
                    "⚠️ Gemini AI is currently busy.\n\n"
                    "Please wait a minute and try again."
                )

            return f"❌ Error:\n\n{error}"

    return "⚠️ Failed to generate interview questions."