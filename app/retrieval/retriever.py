from app.vectorstore.faiss_store import create_faiss_index, search_index


def retrieve_documents(
        query,
        documents,
        embed_fn,
        top_k=3,
        filters=None):

    filtered_docs = apply_filters(
        documents,
        filters
    )

    if not filtered_docs:
        raise ValueError(
            f"No documents matched the requested filters: {filters}"
        )

    texts = [
        doc["text"]
        for doc in filtered_docs
    ]

    embeddings = embed_fn(
        texts
    )

    index = create_faiss_index(
        embeddings
    )

    query_embedding = embed_fn(
        [query]
    )

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(filtered_docs))
    )

    retrieved_docs = []

    for score, idx in zip(scores[0], indices[0]):
        doc = filtered_docs[idx].copy()
        doc["faiss_score"] = float(score)
        retrieved_docs.append(doc)

    return retrieved_docs

def apply_filters(
        documents,
        filters):

    if filters is None:
        return documents

    filtered_docs = []

    for doc in documents:

        matched = True

        for key, value in filters.items():

            if doc.get(key) != value:
                matched = False
                break

        if matched:
            filtered_docs.append(doc)

    return filtered_docs
