from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Optional, Sequence


class DocumentLoader:
    def __init__(self, source_paths: Optional[Sequence[str | Path]] = None):
        self.source_paths = [Path(p) for p in (source_paths or [])]

    def load(self) -> List[str]:
        documents: List[str] = []
        for path in self.source_paths:
            if not path.exists():
                continue
            if path.is_dir():
                documents.extend(self._load_from_directory(path))
            else:
                documents.extend(self._load_single_file(path))
        return documents

    def _load_from_directory(self, path: Path) -> List[str]:
        documents: List[str] = []
        for file_path in sorted(path.rglob("*")):
            if file_path.is_file():
                documents.extend(self._load_single_file(file_path))
        return documents

    def _load_single_file(self, path: Path) -> List[str]:
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            return [path.read_text(encoding="utf-8")]
        if suffix == ".pdf":
            return self._load_pdf(path)
        if suffix == ".db":
            return self._load_sqlite(path)
        return []

    def _load_pdf(self, path: Path) -> List[str]:
        try:
            import PyPDF2  # type: ignore
        except ImportError:
            return []

        reader = PyPDF2.PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return ["\n".join(page for page in pages if page).strip()]

    def _load_sqlite(self, path: Path) -> List[str]:
        try:
            conn = sqlite3.connect(str(path))
            try:
                rows = conn.execute("SELECT content FROM documents").fetchall()
            finally:
                conn.close()
        except sqlite3.Error:
            return []
        return [row[0] for row in rows if row and row[0]]
