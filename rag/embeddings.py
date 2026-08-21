from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return embedding_model


if __name__ == "__main__":
    embeddings = get_embedding_model()

    vector = embeddings.embed_query("Python Machine Learning")

    print(f"Embedding Dimension: {len(vector)}")
    print(vector[:10])