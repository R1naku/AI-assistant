from __future__ import annotations

from typing import List, Sequence

from modules.rag.modules.embeddings import SimpleEmbedding


class SimpleRetriever:
    def __init__(self, chunk_size: int = 100):
        self.chunk_size = chunk_size

    def retrieve(self, question: str, chunks: Sequence[str], top_k: int = 3) -> List[str]:
        if not chunks:
            return []

        normalized_question = question.lower()
        scored = []
        for chunk in chunks:
            score = sum(1 for term in normalized_question.split() if term in chunk.lower())
            scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        best = [chunk for _, chunk in scored if _ > 0][:top_k]
        if best:
            return best
        return list(chunks[:top_k])


class EmbeddingRetriever:
    def __init__(self):
        self.embedding_model = SimpleEmbedding()

    def retrieve(self, question: str, chunks: Sequence[str], top_k: int = 3) -> List[str]:
        if not chunks:
            return []

        question_vector = self.embedding_model.embed(question)
        scored = []
        for chunk in chunks:
            chunk_vector = self.embedding_model.embed(chunk)
            score = self._cosine_similarity(question_vector, chunk_vector)
            scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]

    def _cosine_similarity(self, left: List[float], right: List[float]) -> float:
        if not left or not right:
            return 0.0

        left_norm = sum(value * value for value in left) ** 0.5
        right_norm = sum(value * value for value in right) ** 0.5
        if left_norm == 0 or right_norm == 0:
            return 0.0

        dot = sum(a * b for a, b in zip(left, right))
        return dot / (left_norm * right_norm)
