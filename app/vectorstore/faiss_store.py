import faiss
import numpy as np


def create_faiss_index(embeddings):

    embeddings = np.asarray(embeddings, dtype=np.float32)

    if embeddings.ndim != 2 or embeddings.shape[0] == 0:
        raise ValueError(
            "Embeddings must be a non-empty 2D array."
        )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(
        embeddings
    )

    return index

def search_index(
    index,
    query_embedding,
    top_k=5
):
    scores, indices = index.search(
        np.array(
            query_embedding,
            dtype=np.float32
        ),
        top_k
    )

    return scores, indices
