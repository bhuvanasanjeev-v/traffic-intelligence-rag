def get_sources(
        retrieved_docs):

    return list(
        set(
            doc["source"]
            for doc in retrieved_docs
        )
    )