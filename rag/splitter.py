from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import load_documents


def split_documents():

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"\nTotal Chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:5]):
        print("=" * 60)
        print(f"Chunk {i+1}")
        print(chunk.page_content[:250])

    return chunks


if __name__ == "__main__":
    split_documents()