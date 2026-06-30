from app.ingestion.document_pipeline import DocumentPipeline
from app.rag.rag_pipeline import RAGPipeline


documents = DocumentPipeline(
    "data/raw",
    output_path="data/processed/recursive_chunks.json",
).process()

pipeline = RAGPipeline(documents)

while True:
    query = input("\nAsk your question: ").strip()

    if query.lower() in {"exit", "quit"}:
        break

    result = pipeline.ask(query)
    print("\n" + "=" * 80)
    print("REWRITTEN QUERY")
    print("=" * 80)
    print(result["rewritten_query"])

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for source in result["sources"]:
        print(source)
