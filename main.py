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

import json

text = load_pdf(
    "data/raw/road_safety_new.pdf"
)

print(text[:2000])

# Create a reusable function:

def create_chunk_documents(
    chunks,
    source_file,
    document_type="traffic_report"
):
    documents = []

    for idx, chunk in enumerate(chunks):
        documents.append(
            {
                "chunk_id": idx,
                "source": source_file,
                "document_type": document_type,
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
    "data/raw/road_safety.docx"
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
embeddings = generate_embeddings(text_chunks)
index = create_faiss_index(
    embeddings
)
query = input(
    "\nAsk your question here: "
)
query_embedding = generate_embeddings(
    [query]
)
print("\nQuery:")
print(query)

print("\nFirst 10 values of query embedding:")
print(query_embedding[0][:10])
scores, indices = search_index(
    index,
    query_embedding,
    top_k=3
)

print("\nRetrieved Chunks",indices,scores)
print("=" * 50)

retrieved_docs = []

for idx in indices[0]:
    print("\n")
    print(documents[idx]["text"])
    retrieved_docs.append(documents[idx]    )

context = "\n\n".join(
    doc["text"]
    for doc in retrieved_docs
)
prompt_template = load_prompt_template("rag_answer_prompt.txt")
prompt = prompt_template.format(
    context=context,
    query=query
)
print("prompt is: ", prompt)
llm_runner = LLMRunnerFactory.create_runner("gemini")
answer = llm_runner.run_prompt(prompt)

print("\nLLM Answer:")
print(answer)

print("\nSources:")
print("=" * 50)

for doc in retrieved_docs:
    print(
        f"{doc['source']} "
        f"(Chunk {doc['chunk_id']})"
    )

sources = set()

for doc in retrieved_docs:
    sources.add(doc["source"])

print("\nSources Used:")

for source in sources:
    print(source)

for doc, embedding in zip(
    documents,
    embeddings
):
    doc["embedding"] = embedding.tolist()

with open(
    "data/processed/chunks_with_embeddings.json",
    "w"
) as f:
    json.dump(
        documents,
        f,
        indent=2
    )

