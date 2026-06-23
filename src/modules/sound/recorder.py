import time
from queue import Empty, Queue

import numpy as np
import sounddevice as sd
from config import CHANNELS, DTYPE, SAMPLE_RATE, SEGMENT_SAMPLES, SILENCE_TIMEOUT
from infostructure.ai.llm import generate_response
from infostructure.ai.whisper_stt import transcribe
from modules.sound.vad import is_speech
from modules.ui.console import print_assistant, print_user

audio_queue = Queue()


def callback(indata, frames, time_info, status):
    if status:
        print_assistant(f"Audio callback status: {status}")

    audio_queue.put(indata.copy())


def start_microphone():
    print_assistant("Голосовой ассистент слушает...")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        blocksize=SEGMENT_SAMPLES,
        callback=callback
    ):
        speech_chunks = []
        speech_active = False
        last_speech_time = None

        while True:
            try:
                chunk = audio_queue.get(timeout=0.5)
            except Empty:
                chunk = None

            if chunk is None:
                if speech_active and last_speech_time and time.time() - last_speech_time > SILENCE_TIMEOUT:
                    process_speech(speech_chunks)
                    speech_chunks = []
                    speech_active = False
                continue

            frame_bytes = chunk.flatten().tobytes()
            if is_speech(frame_bytes):
                speech_chunks.append(frame_bytes)
                last_speech_time = time.time()
                speech_active = True
                continue

            if speech_active and last_speech_time and time.time() - last_speech_time > SILENCE_TIMEOUT:
                process_speech(speech_chunks)
                speech_chunks = []
                speech_active = False


def process_speech(chunks):
    if not chunks:
        return

    audio_data = np.frombuffer(b"".join(chunks), dtype=np.int16)

    try:
        text = transcribe(audio_data)
    except Exception as exc:
        print_assistant(f"Ошибка транскрипции: {exc}")
        return

    if not text:
        print_assistant("Не удалось распознать речь.")
        return

    print_user(text)

    try:
        answer = generate_response(text)
    except Exception as exc:
        print_assistant(f"Ошибка LLM: {exc}")
        return

    print_assistant(answer)
