# main.py

from app.document_loader import load_pdf

from app.chunking.chunker import recursive_chunk_text

from app.retrieval.retriever import retrieve_documents
from app.retrieval.bm25_retriever import bm25_search
from app.retrieval.hybrid_retriever import hybrid_retrieve

from app.reranker.reranker import rerank_documents

from app.embeddings.embedder import generate_embeddings

from app.utils.context_builder import build_context
from app.utils.prompt_builder import build_prompt
from app.utils.generate_answer import generate_answer
from app.utils.source_utils import get_sources

import json


def create_chunk_documents(
    chunks,
    source_file,
    document_type,
    site,
    year,
):
    documents = []

    for idx, chunk in enumerate(chunks):
        documents.append(
            {
                "chunk_id": idx,
                "source": source_file,
                "document_type": document_type,
                "site": site,
                "year": year,
                "text": chunk,
            }
        )

    return documents


# ---------------------------------------
# Load Document
# ---------------------------------------

text = load_pdf("data/raw/road_safety_new.pdf")

chunks = recursive_chunk_text(text)

documents = create_chunk_documents(
    chunks=chunks,
    source_file="road_safety_new.pdf",
    document_type="road_safety",
    site="Junction_B",
    year=2025,
)

# Optional - Save chunks for inspection
with open(
    "data/processed/recursive_chunks.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        documents,
        f,
        indent=4,
        ensure_ascii=False,
    )

# ---------------------------------------
# Chat History
# ---------------------------------------

chat_history = []

# ---------------------------------------
# User Query
# ---------------------------------------

query = input("\nAsk your question: ")

# ---------------------------------------
# Metadata Filters
# ---------------------------------------

filters = {
    "site": "Junction_B"
}

# ---------------------------------------
# FAISS Retrieval
# ---------------------------------------

faiss_docs = retrieve_documents(
    query=query,
    documents=documents,
    embed_fn=generate_embeddings,
    top_k=5,
    filters=filters,
)

# ---------------------------------------
# BM25 Retrieval
# ---------------------------------------

bm25_docs = bm25_search(
    query=query,
    documents=documents,
    top_k=5,
    filters=filters,
)

# ---------------------------------------
# Hybrid Retrieval
# ---------------------------------------

candidate_docs = hybrid_retrieve(
    query=query,
    faiss_docs=faiss_docs,
    bm25_docs=bm25_docs,
)

# ---------------------------------------
# Re-rank
# ---------------------------------------

reranked_docs = rerank_documents(
    query=query,
    documents=candidate_docs,
    top_k=3,
)

# ---------------------------------------
# Build Context
# ---------------------------------------

context = build_context(reranked_docs)

# ---------------------------------------
# Build Prompt
# ---------------------------------------

prompt = build_prompt(
    "rag_answer_prompt.txt",
    context,
    query,
)

# ---------------------------------------
# Generate Answer
# ---------------------------------------

answer = generate_answer(prompt)

# ---------------------------------------
# Sources
# ---------------------------------------

sources = get_sources(reranked_docs)

# ---------------------------------------
# Update Chat History
# ---------------------------------------

chat_history.append(
    {
        "role": "user",
        "content": query,
    }
)

chat_history.append(
    {
        "role": "assistant",
        "content": answer,
    }
)

# ---------------------------------------
# Output
# ---------------------------------------

print("\n" + "=" * 80)
print("ANSWER")
print("=" * 80)
print(answer)

print("\n" + "=" * 80)
print("SOURCES")
print("=" * 80)

for source in sources:
    print(source)