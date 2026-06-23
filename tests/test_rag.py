import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from modules.rag.modules.application import RAGApplication
from modules.rag.modules.chunker import WordChunker
from modules.rag.modules.loader import DocumentLoader
from modules.rag.modules.retriever import EmbeddingRetriever


class RAGApplicationTests(unittest.TestCase):
    def test_chunking_splits_text_into_expected_chunks(self):
        chunker = WordChunker(max_words=100)
        text = " ".join([f"word{i}" for i in range(250)])

        chunks = chunker.chunk(text)

        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(len(chunk.split()) <= 100 for chunk in chunks))

    def test_answer_uses_retrieved_context(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            knowledge_path = Path(tmpdir) / "knowledge.txt"
            knowledge_path.write_text(
                "Paris is the capital of France. France is a country in Europe.",
                encoding="utf-8",
            )

            def fake_llm(prompt: str) -> str:
                return prompt

            app = RAGApplication(
                source_paths=[knowledge_path],
                llm_client=fake_llm,
                chunk_size=100,
            )

            answer = app.answer("What is the capital of France?")

            self.assertIn("Paris", answer)
            self.assertIn("France", answer)

    def test_embedding_retriever_prefers_semantically_related_chunk(self):
        retriever = EmbeddingRetriever()
        chunks = [
            "The Eiffel Tower is located in Paris.",
            "Apples are usually red or green.",
        ]

        retrieved = retriever.retrieve("Where is the Eiffel Tower?", chunks, top_k=1)

        self.assertEqual(retrieved[0], chunks[0])

    def test_loader_reads_sqlite_documents(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "knowledge.db"
            conn = sqlite3.connect(str(db_path))
            try:
                conn.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, content TEXT)")
                conn.execute("INSERT INTO documents (content) VALUES (?)", ["The sky is blue."])
                conn.commit()
            finally:
                conn.close()

            loader = DocumentLoader([db_path])
            documents = loader.load()

            self.assertEqual(documents[0], "The sky is blue.")


if __name__ == "__main__":
    unittest.main()
