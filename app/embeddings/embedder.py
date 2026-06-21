from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_embeddings(texts):
    return model.encode(
        texts,
        normalize_embeddings=True
    )