def hybrid_retrieve(
        query,
        faiss_docs,
        bm25_docs,
        top_k=5,
        faiss_weight=0.6,
        bm25_weight=0.4):

    combined = {}

    for doc in faiss_docs:
        chunk_id = doc["chunk_id"]
        combined[chunk_id] = doc.copy()
        combined[chunk_id]["faiss_score"] = doc.get(
            "faiss_score",
            0.0
        )
        combined[chunk_id]["bm25_score"] = 0.0

    for doc in bm25_docs:
        chunk_id = doc["chunk_id"]

        if chunk_id not in combined:
            combined[chunk_id] = doc.copy()
            combined[chunk_id]["faiss_score"] = 0.0

        combined[chunk_id]["bm25_score"] = doc.get(
            "bm25_score",
            0.0
        )

    docs = list(combined.values())

    faiss_scores = [
        doc["faiss_score"]
        for doc in docs
    ]
    bm25_scores = [
        doc["bm25_score"]
        for doc in docs
    ]

    for doc in docs:
        normalized_faiss_score = normalize_score(
            doc["faiss_score"],
            faiss_scores
        )
        normalized_bm25_score = normalize_score(
            doc["bm25_score"],
            bm25_scores
        )

        doc["hybrid_score"] = (
            faiss_weight * normalized_faiss_score
            + bm25_weight * normalized_bm25_score
        )

    return sorted(
        docs,
        key=lambda doc: doc["hybrid_score"],
        reverse=True
    )[:top_k]


def normalize_score(score, all_scores):

    min_score = min(all_scores)
    max_score = max(all_scores)

    if max_score == min_score:
        return 1.0 if score > 0 else 0.0

    return (score - min_score) / (max_score - min_score)
