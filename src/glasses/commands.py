from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/drive"]


class CommandHandler:
    """Interprets voice commands and updates the shared Drive image."""

    def __init__(
        self,
        service_account_file: str,
        image_file_id: str,
        wake_word: str,
    ):
        self.image_file_id = image_file_id
        self.wake_word = wake_word.lower().strip()

        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=SCOPES,
        )
        self.drive = build("drive", "v3", credentials=credentials)

    def is_triggered(self, text: str) -> bool:
        return self.wake_word in text.lower()

    def should_capture(self, text: str) -> bool:
        normalized = text.lower()
        commands = ("وصف", "describe", "capture", "photo", "picture", self.wake_word)
        return any(command in normalized for command in commands)

    def upload_image(self, image_path: str) -> None:
        media = MediaFileUpload(image_path, mimetype="image/jpeg")
        self.drive.files().update(
            fileId=self.image_file_id,
            media_body=media,
        ).execute()

    def handle(self, text: str, camera) -> bool:
        """Returns True when a capture/upload was requested."""
        if not self.is_triggered(text) and not self.should_capture(text):
            return False

        image_path = camera.capture_image("captured_image.jpg")
        self.upload_image(image_path)
        print(f"Image uploaded to Google Drive: {Path(image_path).resolve()}")
        return True
