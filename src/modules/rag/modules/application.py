from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Optional, Sequence

from modules.rag.modules.pipeline import RAGPipeline


class RAGApplication:
    def __init__(
        self,
        source_paths: Optional[Sequence[str | Path]] = None,
        llm_client: Optional[Callable[[str], str]] = None,
        chunk_size: int = 100,
    ):
        self.source_paths = [Path(p) for p in (source_paths or [])]
        self.llm_client = llm_client
        self.chunk_size = chunk_size
        self.pipeline = RAGPipeline(
            source_paths=[str(path) for path in self.source_paths],
            llm_client=llm_client,
            chunk_size=chunk_size,
        )

    def answer(self, question: str, documents: Optional[List[str]] = None) -> str:
        if documents:
            from modules.rag.modules.chunker import WordChunker
            from modules.rag.modules.retriever import SimpleRetriever

            chunker = WordChunker(max_words=self.chunk_size)
            retriever = SimpleRetriever(chunk_size=self.chunk_size)
            chunks = []
            for doc in documents:
                chunks.extend(chunker.chunk(doc))
            context = "\n\n".join(retriever.retrieve(question, chunks))
            from modules.rag.modules.prompt import prompt

            rendered_prompt = prompt.format(context=context, input=question)
            if self.llm_client is None:
                from infostructure.ai.llm import generate_response
                return generate_response(rendered_prompt)
            return self.llm_client(rendered_prompt)

        return self.pipeline.answer(question)
