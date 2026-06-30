from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "BAAI/bge-reranker-base"
)

def rerank_documents(
        query,
        documents,
        top_k=3):

    pairs = [
        (query, doc["text"])
        for doc in documents
    ]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        doc
        for doc, score in ranked[:top_k]
    ]