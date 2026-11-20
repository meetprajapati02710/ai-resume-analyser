from retriever import load_retriever
from llm_chat import ask_resume_ai


retriever = load_retriever()


def ask_rag(
    resume_text,
    job_description,
    user_question
):
    # Retrieve relevant documents
    docs = retriever.invoke(user_question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Combine retrieved knowledge with the user question
    enhanced_question = f"""
Use ONLY the following knowledge while answering.

Knowledge:
{context}

User Question:
{user_question}
"""

    response = ask_resume_ai(
        resume_text,
        job_description,
        enhanced_question
    )

    return response