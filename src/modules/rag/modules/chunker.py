from __future__ import annotations

from typing import List


class WordChunker:
    def __init__(self, max_words: int = 100):
        self.max_words = max_words

    def chunk(self, text: str) -> List[str]:
        words = text.split()
        if not words:
            return []

        chunks: List[str] = []
        for index in range(0, len(words), self.max_words):
            chunk = words[index:index + self.max_words]
            chunks.append(" ".join(chunk))
        return chunks
