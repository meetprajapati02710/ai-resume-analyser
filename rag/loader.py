from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader


def load_documents():

    loader = DirectoryLoader(
        "knowledge_base",
        glob="**/*.md",
        loader_cls=TextLoader
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents.")

    return documents


if __name__ == "__main__":
    docs = load_documents()

    for doc in docs:
        print("=" * 50)
        print(doc.metadata["source"])