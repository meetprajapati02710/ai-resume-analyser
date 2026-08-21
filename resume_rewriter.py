from llm_chat import ask_resume_ai


def rewrite_resume_bullet(
    resume_text,
    bullet
):
    prompt = f"""
You are an expert Resume Writer.

Rewrite the following resume bullet.

Requirements:

• Make it ATS friendly.
• Use strong action verbs.
• Add measurable impact if possible.
• Keep it concise.
• Keep it truthful.
• Return ONLY the improved bullet.

Resume:

{resume_text}

Bullet:

{bullet}
"""

    return ask_resume_ai(
        resume_text=resume_text,
        job_description="",
        user_question=prompt,
        retrieved_context=""
    )