def build_context(
        retrieved_docs):

    return "\n\n".join(
        doc["text"]
        for doc in retrieved_docs
    )