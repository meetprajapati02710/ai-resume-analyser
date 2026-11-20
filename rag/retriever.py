
from pathlib import Path

from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embedding_model

from langsmith import traceable
from tracing_utils import (
    safe_trace_inputs,
    safe_trace_outputs
)


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VECTOR_DB_PATH = PROJECT_ROOT / "vector_db"

# Retrieval configuration
TOP_K = 3


def load_vector_store():

    if not VECTOR_DB_PATH.exists():
        raise FileNotFoundError(
            f"FAISS database not found: {VECTOR_DB_PATH}. "
            "Please build the vector database first."
        )

    print("Loading embedding model...")

    embeddings = get_embedding_model()

    print("Loading FAISS vector database...")

    vector_store = FAISS.load_local(
        str(VECTOR_DB_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS vector database loaded successfully.")

    return vector_store


# Load FAISS once when the module is initialized
vector_store = load_vector_store()


@traceable(
    name="FAISS Context Retrieval",
    run_type="retriever",
    process_inputs=safe_trace_inputs,
    process_outputs=safe_trace_outputs
)
def retrieve_context(question, k=TOP_K):

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    # Step 1: Retrieve relevant documents
    docs = vector_store.similarity_search(
        query=question,
        k=k
    )

    if not docs:
        return "", []

    # Step 2: Extract retrieved context
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Step 3: Extract source metadata
    sources = [
        doc.metadata.get("source", "Unknown")
        for doc in docs
    ]

    return context, sources


if __name__ == "__main__":

    test_question = "What skills are required for an AI/ML Engineer?"

    context, sources = retrieve_context(test_question)

    print("\n========== RETRIEVAL RESULTS ==========")
    print("Question:", test_question)
    print("\nRetrieved sources:")

    for source in sources:
        print("-", source)

    print("\nRetrieved context:")
    print(context)
