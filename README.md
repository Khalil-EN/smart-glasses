# Smart Glasses Assistive Prototype

A Raspberry Pi-based smart-glasses prototype designed to assist blind and visually impaired users through:

- Voice commands captured with a microphone
- Camera-based image capture
- Google Drive as the communication bridge
- OCR performed on captured images
- Text-to-speech audio feedback
- Ultrasonic obstacle detection with a buzzer

## Architecture

The complete prototype runs on a **Raspberry Pi**.

```text
                         RASPBERRY PI
                              |
             +----------------+----------------+
             |                |                |
          Camera          Microphone      Ultrasonic
             |                |             sensor
             v                v                v
         camera.py       speech.py       ultrasonic_sensor.py
             |                |
             +-------+--------+
                     v
                  main.py
                     |
              Voice command
                     |
              Capture image
                     |
                     v
                Google Drive
                     |
                     v
              drive_monitor.py
                     |
                     v
                 processor.py
                     |
                 +---+---+
                 |       |
                 v       v
               ocr.py   TTS
                         |
                         v
                      Speaker
```

The image-capture and image-processing components are separate programs, but both run on the same Raspberry Pi.

## Project structure

```text
smart-glasses/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── src/
│   ├── glasses/
│   │   ├── main.py
│   │   ├── camera.py
│   │   ├── speech.py
│   │   └── commands.py
│   │
│   ├── processing/
│   │   ├── drive_monitor.py
│   │   ├── ocr.py
│   │   └── processor.py
│   │
│   └── hardware/
│       └── ultrasonic_sensor.py
│
├── docs/
│   └── architecture.md
│
└── legacy/
    └── README.md
```

## Components

### Glasses

`src/glasses/main.py` is the main loop. It coordinates speech recognition, command handling, and image capture.

- `camera.py`: captures images from the connected camera.
- `speech.py`: records microphone input and sends it to Whisper for transcription.
- `commands.py`: interprets recognized commands and triggers the appropriate action.

### Processing

The processing side monitors the Google Drive image used by the prototype.

- `drive_monitor.py`: detects when the configured image is modified and downloads it.
- `ocr.py`: extracts text from the image using Tesseract.
- `processor.py`: connects the download, OCR, and text-to-speech steps.

### Hardware

`src/hardware/ultrasonic_sensor.py` reads an ultrasonic sensor and activates a buzzer when an obstacle is closer than the configured threshold.

## Requirements

The prototype requires:

- Raspberry Pi
- Camera compatible with the Raspberry Pi/OpenCV
- Microphone
- Speaker/audio output
- Ultrasonic distance sensor
- Buzzer
- Internet connection for Google Drive and Whisper/gTTS services
- Python 3
- Tesseract OCR installed on the Raspberry Pi

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

For Raspberry Pi GPIO support, install the appropriate GPIO package for the Raspberry Pi OS version being used.

Tesseract itself is a system package and is not installed by `pip`.

## Google Drive setup

1. Create a Google Cloud project.
2. Enable the Google Drive API.
3. Create a service account.
4. Download its JSON credentials.
5. Create/share the Google Drive folder used by the prototype with the service account.
6. Create or upload the image file that the prototype will update.
7. Put the credentials somewhere outside version control, for example:

```text
credentials/service_account.json
```

8. Copy `.env.example` to `.env`.
9. Fill in the required IDs and API key.


## Configuration

The main environment variables are:

```text
OPENAI_API_KEY
GOOGLE_DRIVE_FOLDER_ID
GOOGLE_DRIVE_IMAGE_FILE_ID
GOOGLE_SERVICE_ACCOUNT_FILE
WAKE_WORD
POLL_INTERVAL_SECONDS
OCR_LANGUAGE
TTS_LANGUAGE
TRIG_PIN
ECHO_PIN
BUZZER_PIN
THRESHOLD_DISTANCE_CM
```

The Google Drive image file ID identifies the image updated by the glasses program.

## Running the prototype

From the repository root:

### 1. Start the glasses application

```bash
python src/glasses/main.py
```

This starts the microphone/speech loop. When the configured wake word or supported command is detected, the camera captures an image and uploads/updates it on Google Drive.

### 2. Start the image processor

In another terminal:

```bash
python src/processing/drive_monitor.py
```

The processor monitors the configured Google Drive image. When it changes, it downloads the new image, performs OCR, and converts the recognized text to speech.

### 3. Start obstacle detection

In another terminal:

```bash
python src/hardware/ultrasonic_sensor.py
```

The ultrasonic sensor runs independently and activates the buzzer when an obstacle is closer than the configured threshold.


## Original workflow

The original prototype was built around a simple distributed-by-function design:

```text
Microphone
   |
   v
Speech recognition
   |
   v
Wake word / command
   |
   v
Camera capture
   |
   v
Google Drive
   |
   v
Drive monitor
   |
   v
Image download
   |
   v
Tesseract OCR
   |
   v
Text-to-speech
   |
   v
Speaker
```

The ultrasonic system works independently:

```text
Ultrasonic sensor
       |
       v
Distance measurement
       |
   distance < threshold
       |
       v
     Buzzer
```

## Why Google Drive?

Google Drive was used as a simple communication bridge between the image-capture and processing components.

For a future version, this could be replaced with a more direct mechanism such as:

- Local filesystem communication
- HTTP API
- MQTT
- Message queue
- Local IPC

Google Drive is retained here because it is part of the original prototype architecture.

## Limitations

This repository represents a cleaned and modular reconstruction of an older prototype. It is not a production-ready assistive device.

Known limitations include:

- Network dependency for Google Drive
- Network/API dependency for speech recognition and gTTS
- Polling instead of event-driven Google Drive notifications
- Basic command matching
- Basic OCR preprocessing
- No robust background-process/service management
- No complete hardware enclosure or power-management design
- No comprehensive automated test suite
- Camera, microphone, and audio configuration may require Raspberry Pi-specific adjustments

## Future improvements

Potential improvements include:

- Offline speech recognition
- Offline text-to-speech
- Better wake-word detection
- Better OCR preprocessing
- Object detection and scene description
- GPS/location awareness
- Haptic feedback
- More reliable asynchronous processing
- A local communication mechanism instead of Google Drive
- systemd services for automatic startup
- Unit and integration tests
- Better error handling and logging

## Project history

This project started as an assistive smart-glasses prototype. The original implementation was a collection of scripts for camera capture, speech recognition, Google Drive synchronization, OCR, TTS, and ultrasonic obstacle detection.

The current `src/` directory reorganizes those ideas into smaller modules with clearer responsibilities. The `legacy/` directory is reserved for documentation and, if desired, the original prototype scripts.

## Disclaimer

This is an educational/prototype project. It should not be relied upon as the sole navigation or safety system for a person with a visual impairment.
