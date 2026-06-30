import json
from pathlib import Path

from app.chunking.chunker import recursive_chunk_text
from app.ingestion.document_loader import load_docx, load_excel, load_pdf
from app.ingestion.metadata_parser import parse_metadata_from_filename


class DocumentPipeline:
    """Load, chunk, and enrich every supported file in a raw data directory."""

    LOADERS = {
        ".pdf": load_pdf,
        ".xlsx": load_excel,
        ".xls": load_excel,
        ".docx": load_docx,
    }

    def __init__(
        self,
        raw_dir,
        chunk_size=1000,
        chunk_overlap=100,
        output_path=None,
    ):
        self.raw_dir = Path(raw_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.output_path = Path(output_path) if output_path else None

    def process(self):
        documents = []

        for file_path in self._iter_supported_files():
            documents.extend(
                self._process_file(
                    file_path,
                    starting_chunk_id=len(documents),
                )
            )

        if self.output_path:
            self._save_documents(documents)

        return documents

    def _iter_supported_files(self):
        if not self.raw_dir.exists():
            raise FileNotFoundError(f"Raw data path not found: {self.raw_dir}")

        if self.raw_dir.is_file():
            files = [self.raw_dir]
        else:
            files = sorted(
                file_path
                for file_path in self.raw_dir.rglob("*")
                if file_path.is_file()
            )

        return [
            file_path
            for file_path in files
            if file_path.suffix.lower() in self.LOADERS
        ]

    def _process_file(self, file_path, starting_chunk_id):
        text = self._load_document(file_path)
        chunks = recursive_chunk_text(
            text,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        metadata = parse_metadata_from_filename(file_path)

        return self._create_documents(
            chunks=chunks,
            source_file=file_path.name,
            metadata=metadata,
            starting_chunk_id=starting_chunk_id,
        )

    def _load_document(self, file_path):
        extension = file_path.suffix.lower()
        loader = self.LOADERS.get(extension)

        if loader is None:
            supported = ", ".join(sorted(self.LOADERS))
            raise ValueError(
                f"Unsupported document type '{extension}'. Supported types: {supported}"
            )

        return loader(str(file_path))

    def _create_documents(
        self,
        chunks,
        source_file,
        metadata,
        starting_chunk_id,
    ):
        documents = []

        for idx, chunk in enumerate(chunks):
            documents.append(
                {
                    "chunk_id": starting_chunk_id + idx,
                    "source": source_file,
                    "document_type": metadata["document_type"],
                    "site": metadata["site"],
                    "year": metadata["year"],
                    "text": chunk,
                }
            )

        return documents

    def _save_documents(self, documents):
        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.output_path.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                documents,
                f,
                indent=4,
                ensure_ascii=False,
            )
