import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import settings
from src.glasses.camera import Camera
from src.glasses.commands import CommandHandler
from src.glasses.speech import SpeechRecognizer


def main() -> None:
    settings.require(
        settings.OPENAI_API_KEY,
        settings.GOOGLE_DRIVE_IMAGE_FILE_ID,
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
    )

    camera = Camera()
    speech = SpeechRecognizer(settings.OPENAI_API_KEY)
    commands = CommandHandler(
        service_account_file=settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        image_file_id=settings.GOOGLE_DRIVE_IMAGE_FILE_ID,
        wake_word=settings.WAKE_WORD,
    )

    print("Smart-glasses voice interface started.")
    print(f"Wake word: {settings.WAKE_WORD!r}")

    try:
        while True:
            text = speech.listen()
            if not text:
                continue

            print(f"Recognized: {text}")

            if commands.handle(text, camera):
                print("Capture request completed.")
    except KeyboardInterrupt:
        print("\nStopping glasses application.")
    finally:
        camera.close()


if __name__ == "__main__":
    main()
