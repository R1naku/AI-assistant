import threading
import time

from modules.sound.recorder import start_microphone
from modules.ui.console import print_assistant


if __name__ == "__main__":
    print_assistant("Ассистент запущен")

    threading.Thread(
        target=start_microphone,
        daemon=True
    ).start()

    while True:
        time.sleep(1)
