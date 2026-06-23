from __future__ import annotations

from typing import Callable, List, Optional, Sequence

from modules.rag.modules.chunker import WordChunker
from modules.rag.modules.loader import DocumentLoader
from modules.rag.modules.prompt import prompt
from modules.rag.modules.retriever import EmbeddingRetriever


class RAGPipeline:
    def __init__(
        self,
        source_paths: Optional[Sequence[str]] = None,
        llm_client: Optional[Callable[[str], str]] = None,
        chunk_size: int = 100,
    ):
        self.source_paths = list(source_paths or [])
        self.llm_client = llm_client
        self.chunker = WordChunker(max_words=chunk_size)
        self.retriever = EmbeddingRetriever()
        self.loader = DocumentLoader(self.source_paths)

    def answer(self, question: str) -> str:
        documents = self.loader.load()
        chunks = []
        for document in documents:
            chunks.extend(self.chunker.chunk(document))

        relevant = self.retriever.retrieve(question, chunks)
        context = "\n\n".join(relevant)
        rendered_prompt = prompt.format(context=context, input=question)

        if self.llm_client is None:
            from infostructure.ai.llm import generate_response
            return generate_response(rendered_prompt)
        return self.llm_client(rendered_prompt)
