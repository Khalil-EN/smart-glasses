import os
import time
import wave
from pathlib import Path

import pyaudio
from openai import OpenAI


class SpeechRecognizer:

    def __init__(
        self,
        api_key: str,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
    ):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required.")

        self.client = OpenAI(api_key=api_key)
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size

    def record_until_silence(
        self,
        output_path: str = "command.wav",
        silence_seconds: float = 1.0,
        max_seconds: float = 10.0,
    ) -> str:
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        frames = []
        started = time.monotonic()
        last_audio = started

        try:
            while time.monotonic() - started < max_seconds:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)

                samples = memoryview(data).cast("h")
                peak = max((abs(sample) for sample in samples), default=0)

                if peak > 500:
                    last_audio = time.monotonic()
                elif frames and time.monotonic() - last_audio >= silence_seconds:
                    break
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

        path = Path(output_path)
        with wave.open(str(path), "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(b"".join(frames))

        return str(path)

    def transcribe(self, audio_path: str) -> str:
        with open(audio_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
        return response.text.strip()

    def listen(self) -> str:
        audio_path = self.record_until_silence()
        try:
            return self.transcribe(audio_path)
        finally:
            try:
                os.remove(audio_path)
            except OSError:
                pass
