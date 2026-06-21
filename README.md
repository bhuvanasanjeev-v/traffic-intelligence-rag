# Traffic Intelligence RAG Assistant

An end-to-end Retrieval-Augmented Generation (RAG) system for querying traffic reports, Excel survey data, and client documents using semantic search and LLMs.

---

## Features

- PDF, Excel and DOCX document ingestion
- Multiple chunking strategies
- Embedding generation
- FAISS vector database
- Semantic similarity search
- Metadata filtering
- Hybrid retrieval (planned)
- Reranking (planned)
- RAG evaluation (planned)
- Executive summary generation

---

## Architecture

```text
Documents
    ↓
Document Loaders
    ↓
Chunking
    ↓
Embeddings
    ↓
FAISS Vector Store
    ↓
Retriever
    ↓
LLM
    ↓
Response
```

---

## Tech Stack

| Component | Technology |
|------------|------------|
| Language | Python |
| Framework | LangChain |
| Embeddings | BGE Small |
| Vector Database | FAISS |
| LLM | Gemini 2.5 Flash |
| Evaluation | RAGAS |
| Frontend | Streamlit |
| API | FastAPI |

---

## Project Structure

```text
traffic-intelligence-rag/
├── app/
├── data/
├── notebooks/
├── tests/
├── configs/
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/<username>/traffic-intelligence-rag.git

cd traffic-intelligence-rag

python -m venv venv

pip install -r requirements.txt
```

---

## Example Queries

- What was the peak hour volume at Junction A?
- Compare traffic between Site A and Site B.
- Summarize pedestrian observations.
- Generate executive summary for the client.

---

## Roadmap

### Phase 1
- [x] Document ingestion
- [x] Chunking
- [x] Embeddings
- [x] FAISS
- [x] Similarity search

### Phase 2
- [ ] Metadata filtering
- [ ] Hybrid retrieval
- [ ] BM25 search
- [ ] Reranking

### Phase 3
- [ ] Multi-query retrieval
- [ ] Query rewriting
- [ ] Context compression
- [ ] RAGAS evaluation

### Phase 4
- [ ] Streamlit UI
- [ ] FastAPI backend
- [ ] Docker deployment
- [ ] Qdrant integration

---

## Future Improvements

- Hybrid Search
- Re-ranking
- Multi-query Retrieval
- Parent-Child Retrieval
- Query Expansion
- RAGAS Evaluation
- Docker Support

---

## License

MIT License
