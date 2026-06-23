import webrtcvad
from config import SAMPLE_RATE


vad = webrtcvad.Vad()
vad.set_mode(1)


def is_speech(frame):

    try:
        return vad.is_speech(
            frame,
            SAMPLE_RATE
        )

    except:
        return False