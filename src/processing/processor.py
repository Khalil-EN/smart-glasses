import os
from pathlib import Path

from gtts import gTTS
from pygame import mixer

from src.processing.ocr import extract_text


class ImageProcessor:
    """Runs OCR and converts the recognized text to speech."""

    def __init__(self, ocr_language: str = "eng", tts_language: str = "en"):
        self.ocr_language = ocr_language
        self.tts_language = tts_language

    def speak(self, text: str, output_path: str = "ocr_output.mp3") -> None:
        if not text:
            print("OCR produced no text.")
            return

        tts = gTTS(text=text, lang=self.tts_language)
        tts.save(output_path)

        mixer.init()
        try:
            mixer.music.load(output_path)
            mixer.music.play()

            while mixer.music.get_busy():
                pass
        finally:
            mixer.music.stop()
            mixer.quit()

        try:
            os.remove(output_path)
        except OSError:
            pass

    def process(self, image_path: str) -> str:
        print(f"Processing image: {Path(image_path).resolve()}")

        text = extract_text(
            image_path,
            language=self.ocr_language,
        )

        print("OCR result:")
        print(text if text else "[No text detected]")

        if text:
            self.speak(text)

        return text
