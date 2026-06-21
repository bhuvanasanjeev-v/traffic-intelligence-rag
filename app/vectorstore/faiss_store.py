import faiss
import numpy as np


def create_faiss_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(
        np.array(embeddings, dtype=np.float32)
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