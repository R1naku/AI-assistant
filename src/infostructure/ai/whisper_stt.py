import numpy as np

from config import SAMPLE_RATE, WHISPER_MODEL

try:
    import whisper as _whisper
except Exception as _import_error:
    _whisper = None
    whisper_import_error = _import_error

_model = None


def _load_model():
    global _model
    if _model is None:
        if _whisper is None:
            raise RuntimeError(
                "OpenAI Whisper is not available. Install the openai-whisper package and remove the conflicting whisper package.. "
                f"error: {whisper_import_error}"
            )

        _model = _whisper.load_model(WHISPER_MODEL, device="cpu")

    return _model


def transcribe(audio_data):
    if not isinstance(audio_data, np.ndarray):
        raise TypeError("audio data must be a NumPy array of int16 samples.")

    if audio_data.dtype != np.int16:
        audio_data = audio_data.astype(np.int16)

    model = _load_model()
    audio = audio_data.astype(np.float32) / np.iinfo(np.int16).max

    result = model.transcribe(
        audio,
        fp16=False,
        language="ru",
    )
    

    return result.get("text", "").strip()
