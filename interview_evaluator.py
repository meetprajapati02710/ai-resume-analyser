from llm_chat import ask_resume_ai


def evaluate_answer(
    resume_text,
    job_description,
    question,
    user_answer
):

    prompt = f"""
You are a Senior Technical Interviewer.

Candidate Resume:
{resume_text}

Job Description:
{job_description}

Interview Question:
{question}

Candidate Answer:
{user_answer}

Evaluate the answer using the following format ONLY.

Overall Score: X/10

Technical Accuracy:
(2-3 sentences)

Communication:
(2-3 sentences)

Confidence:
(2-3 sentences)

Strengths:
- Point 1
- Point 2

Areas to Improve:
- Point 1
- Point 2

Keep the evaluation professional.
"""

    return ask_resume_ai(
        resume_text,
        job_description,
        user_question=prompt,
        retrieved_context=""
    )