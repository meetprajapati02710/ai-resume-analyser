
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.loader import load_documents


def split_documents():

    # Step 1: Load documents from knowledge_base
    print("\nLoading documents...")

    documents = load_documents()

    if not documents:
        raise ValueError("No documents found in knowledge_base!")

    print(f"Loaded {len(documents)} documents.")

    # Step 2: Initialize text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    # Step 3: Split documents into chunks
    print("\nSplitting documents...")

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No chunks were generated!")

    # Step 4: Display statistics
    print("\n========== SPLITTING SUMMARY ==========")
    print(f"Total documents : {len(documents)}")
    print(f"Total chunks    : {len(chunks)}")

    # Step 5: Display sample chunks
    print("\n========== SAMPLE CHUNKS ==========")

    for i, chunk in enumerate(chunks[:5], start=1):

        print(f"\nChunk {i}")
        print("-" * 50)

        print("Source:", chunk.metadata.get("source", "Unknown"))
        print("Characters:", len(chunk.page_content))
        print("Content:", chunk.page_content[:250])

    print("\nDocument splitting completed successfully!")

    return chunks


if __name__ == "__main__":
    split_documents()
