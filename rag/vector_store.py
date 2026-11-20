from langchain_community.vectorstores import FAISS

from loader import load_documents
from splitter import split_documents
from embeddings import get_embedding_model


def build_vector_store():

    print("Loading documents...")
    documents = load_documents()

    print("\nSplitting documents...")
    chunks = split_documents()

    print("\nLoading embedding model...")
    embeddings = get_embedding_model()

    print("\nCreating FAISS Vector Store...")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vector_store.save_local("vector_db")

    print("\n✅ Vector Store Created Successfully")
    print(f"Indexed {len(chunks)} chunks")

    return vector_store


if __name__ == "__main__":
    build_vector_store()