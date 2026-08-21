from llm_chat import ask_resume_ai
from rag.retriever import retrieve_context


def chat_with_resume(
    resume_text,
    job_description,
    user_question
):
    retrieved_context, sources = retrieve_context(user_question)

    answer = ask_resume_ai(
        resume_text=resume_text,
        job_description=job_description,
        user_question=user_question,
        retrieved_context=retrieved_context
    )

    return answer, sources