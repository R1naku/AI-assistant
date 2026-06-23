import threading
import time
from pathlib import Path

from modules.rag.modules.application import RAGApplication
from modules.sound.recorder import start_microphone
from modules.ui.console import print_assistant


if __name__ == "__main__":
    knowledge_dir = Path(__file__).resolve().parent / "knowledge"
    knowledge_dir.mkdir(exist_ok=True)

    rag_app = RAGApplication(source_paths=[knowledge_dir], chunk_size=100)
    print_assistant("assistant running")

    threading.Thread(
        target=start_microphone,
        daemon=True
    ).start()

    while True:
        time.sleep(1)
