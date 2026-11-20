from langsmith import traceable

from llm_chat import ask_resume_ai
from rag.retriever import retrieve_context

from tracing_utils import (
    safe_trace_inputs,
    safe_trace_outputs
)


@traceable(
    name="Resume RAG Pipeline",
    run_type="chain",
    process_inputs=safe_trace_inputs,
    process_outputs=safe_trace_outputs
)
def chat_with_resume(
    resume_text,
    job_description,
    user_question
):

    # Step 1: Retrieve relevant context
    retrieved_context, sources = retrieve_context(
        user_question
    )

    # Step 2: Generate answer using Gemini
    answer = ask_resume_ai(
        resume_text=resume_text,
        job_description=job_description,
        user_question=user_question,
        retrieved_context=retrieved_context
    )

    # Step 3: Return answer and sources
    return answer, sources