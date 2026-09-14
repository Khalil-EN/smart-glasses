import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from config import settings
from src.processing.processor import ImageProcessor


SCOPES = ["https://www.googleapis.com/auth/drive"]


def authenticate():
    settings.require(settings.GOOGLE_SERVICE_ACCOUNT_FILE)

    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )
    return build("drive", "v3", credentials=credentials)


def get_modified_time(service, file_id: str) -> str:
    metadata = service.files().get(
        fileId=file_id,
        fields="id,name,modifiedTime",
    ).execute()
    return metadata["modifiedTime"]


def download_image(service, file_id: str, output_path: str) -> str:
    request = service.files().get_media(fileId=file_id)

    with open(output_path, "wb") as output:
        downloader = MediaIoBaseDownload(output, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    return output_path


def monitor() -> None:
    settings.require(
        settings.GOOGLE_DRIVE_IMAGE_FILE_ID,
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
    )

    service = authenticate()
    processor = ImageProcessor(
        ocr_language=settings.OCR_LANGUAGE,
        tts_language=settings.TTS_LANGUAGE,
    )

    file_id = settings.GOOGLE_DRIVE_IMAGE_FILE_ID
    previous_modified_time = get_modified_time(service, file_id)

    print("Google Drive monitor started.")
    print(f"Watching image file: {file_id}")

    while True:
        try:
            current_modified_time = get_modified_time(service, file_id)

            if current_modified_time != previous_modified_time:
                print("New image detected.")
                image_path = download_image(
                    service,
                    file_id,
                    "received_image.jpg",
                )
                processor.process(image_path)
                previous_modified_time = current_modified_time

        except Exception as exc:
            print(f"Processing error: {exc}")

        time.sleep(settings.POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\nStopping Google Drive monitor.")
