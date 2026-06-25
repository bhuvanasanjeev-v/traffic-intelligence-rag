from rank_bm25 import BM25Okapi
from app.retrieval.retriever import apply_filters


def create_bm25_index(documents):

    corpus = [
        doc["text"].lower().split()
        for doc in documents
    ]

    bm25 = BM25Okapi(corpus)

    return bm25

def bm25_search(
        query,
        documents,
        top_k=5,
        filters=None):

    filtered_docs = apply_filters(
        documents,
        filters
    )

    if not filtered_docs:
        raise ValueError(
            f"No documents matched the requested filters: {filters}"
        )

    bm25 = create_bm25_index(filtered_docs)

    tokens = query.lower().split()

    scores = bm25.get_scores(
        tokens
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    return [
        {
            **filtered_docs[i],
            "bm25_score": float(scores[i])
        }
        for i in ranked_indices[:top_k]
    ]
