# main.py

from app.document_loader import (
    load_pdf,
    load_excel,
    load_docx
)
from app.chunking.chunker import (
    fixed_chunk_text,
    create_chunks_with_metadata,
    recursive_chunk_text
)
from app.embeddings.embedder import generate_embeddings

from app.vectorstore.faiss_store import create_faiss_index, search_index
from llm.llm_factory import LLMRunnerFactory
from llm.prompt_loader import load_prompt_template

from app.retrieval.retriever import retrieve_documents
from app.utils.source_utils import get_sources
from app.utils.context_builder import build_context
from app.utils.prompt_builder import build_prompt
from app.utils.generate_answer import generate_answer

import json

text = load_pdf(
    "data/raw/road_safety_new.pdf"
)

print(text[:2000])

# Create a reusable function:

def create_chunk_documents(
    chunks,
    source_file,
    document_type,
    site,
    year
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
                "text": chunk
            }
        )

    return documents

# chunks = create_chunks_with_metadata(
#     text,
#     "data/raw/junction_data.xlsx"
# )
chunks = recursive_chunk_text(text)
documents = create_chunk_documents(
    chunks,
    source_file="road_safety_new.pdf",
    document_type="road_safety",
    site="Junction_B",
    year=2025
)

with open(
    "data/processed/recursive_chunks.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        documents,
        f,
        indent=4,
        ensure_ascii=False
    )

text_chunks = [
    doc["text"]
    for doc in documents
]

query = input(
    "\nAsk your question here: "
)

retrieved_docs = retrieve_documents(
    query,
    documents,
    generate_embeddings,
    filters={
        "site": "Junction_C"
    }
)

context = build_context(
    retrieved_docs
)

prompt = build_prompt(
    "rag_answer_prompt.txt",
    context,
    query
)

answer = generate_answer(
    prompt
)

sources = get_sources(
    retrieved_docs
)

print("\nAnswer:")
print(answer)

print("\nSources:")
for source in sources:
    print(source)
