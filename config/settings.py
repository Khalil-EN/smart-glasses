import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
GOOGLE_DRIVE_IMAGE_FILE_ID = os.getenv("GOOGLE_DRIVE_IMAGE_FILE_ID", "")
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE",
    "credentials/service_account.json",
)

WAKE_WORD = os.getenv("WAKE_WORD", "hi")
POLL_INTERVAL_SECONDS = _int_env("POLL_INTERVAL_SECONDS", 10)

OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")
TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")

TRIG_PIN = _int_env("TRIG_PIN", 14)
ECHO_PIN = _int_env("ECHO_PIN", 15)
BUZZER_PIN = _int_env("BUZZER_PIN", 16)
THRESHOLD_DISTANCE_CM = _int_env("THRESHOLD_DISTANCE_CM", 20)


def require(*values: str) -> None:
    missing = [
        name
        for name, value in [
            ("OPENAI_API_KEY", OPENAI_API_KEY),
            ("GOOGLE_DRIVE_IMAGE_FILE_ID", GOOGLE_DRIVE_IMAGE_FILE_ID),
            ("GOOGLE_SERVICE_ACCOUNT_FILE", GOOGLE_SERVICE_ACCOUNT_FILE),
        ]
        if value == ""
    ]

    # Explicit arguments are also checked so callers can require specific values.
    if any(value == "" for value in values):
        if not missing:
            raise ValueError("One or more required configuration values are missing.")
        raise ValueError(
            "Missing required configuration: " + ", ".join(sorted(set(missing)))
        )
