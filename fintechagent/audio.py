import sounddevice as sd
import wave
from io import BytesIO
import numpy as np
from .defaults import Audio
import threading
from scipy.io.wavfile import write as writewav
import logging

logger = logging.getLogger(__name__)


class PlayAudio:
    def __init__(self):
        self.can_record = True
        self.bytes_per_sample = {2: np.int16, 4: np.int32}

    def play(self, audio: bytes):
        wav_file = wave.open(BytesIO(audio))
        sample_rate = wav_file.getframerate()
        num_channels = wav_file.getnchannels()
        bytes_per_sample = wav_file.getsampwidth()
        audio_data = wav_file.readframes(wav_file.getnframes())
        dtype = self.bytes_per_sample[bytes_per_sample]
        audio_array = np.frombuffer(audio_data, dtype=dtype)
        if num_channels > 1:
            audio_array = audio_array.reshape(-1, num_channels)

        sd.play(audio_array, samplerate=sample_rate)
        sd.wait()

    def record(self):
        audio_data = []

        def record_audio():
            with sd.InputStream(
                Audio.default_sample_rate, channels=1, dtype=np.int16
            ) as stream:
                while self.can_record:
                    data, _ = stream.read(int(Audio.default_sample_rate * 0.1))
                    audio_data.append(data)

        mini_thread = threading.Thread(target=record_audio)
        logger.info("Started Recording")
        mini_thread.start()
        if input("Press Space and followed by Enter to Stop Recording\n") == " ":
            self.can_record = False
        mini_thread.join()
        self.can_record = True
        np.concatenate(audio_data, axis=0)
        byte_buffer = BytesIO()
        writewav(byte_buffer, Audio.default_sample_rate, audio_data)
        recorded_audio = byte_buffer.getvalue()
        byte_buffer.close()
        return recorded_audio
