from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embedding_model


def load_retriever():
    embeddings = get_embedding_model()

    vector_store = FAISS.load_local(
        "vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


retriever = load_retriever()


def retrieve_context(question):
    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    sources = [
        doc.metadata.get("source", "Unknown")
        for doc in docs
    ]

    return context, sources