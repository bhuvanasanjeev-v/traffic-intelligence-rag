from langchain_text_splitters import RecursiveCharacterTextSplitter

def fixed_chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def create_chunks_with_metadata(
    text,
    source_file,
    chunk_size=500,
    overlap=100
):
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(text):

        end = start + chunk_size

        chunk_text = text[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "source": source_file,
            "text": chunk_text
        })

        chunk_id += 1
        start += chunk_size - overlap

    return chunks

def recursive_chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 100
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    return splitter.split_text(text)