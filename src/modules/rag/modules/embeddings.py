from __future__ import annotations

import re
from collections import Counter
from typing import List


class SimpleEmbedding:
    def __init__(self):
        self.stopwords = {
            "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is", "are", "be",
            "this", "that", "with", "it", "its", "as", "at", "by", "from", "what", "where", "who",
            "when", "why", "how", "do", "does", "did", "can", "could", "would", "should"
        }

    def embed(self, text: str) -> List[float]:
        tokens = [token.lower() for token in re.findall(r"\w+", text) if token.lower() not in self.stopwords]
        counter = Counter(tokens)
        if not counter:
            return []
        total = sum(counter.values())
        return [count / total for count in counter.values()]
