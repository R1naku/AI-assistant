import numpy as np

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = np.int16

SEGMENT_DURATION = 0.02
SEGMENT_SAMPLES = int(SAMPLE_RATE * SEGMENT_DURATION)

SILENCE_TIMEOUT = 1.5

WHISPER_MODEL = "medium"

LLM_URL = "http://localhost:1234/v1/chat/completions"          