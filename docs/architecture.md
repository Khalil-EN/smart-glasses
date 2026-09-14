# Architecture

## Overview

The smart-glasses prototype runs its main components on one Raspberry Pi.

There are three independent responsibilities:

1. Glasses interaction
2. Image processing
3. Obstacle detection

## 1. Glasses interaction

```text
Microphone
    |
    v
speech.py
    |
    v
Whisper transcription
    |
    v
commands.py
    |
    v
camera.py
    |
    v
Google Drive image
```

`main.py` coordinates this flow.

## 2. Image processing

```text
Google Drive
    |
    v
drive_monitor.py
    |
    v
Download image
    |
    v
processor.py
    |
    +----> ocr.py
    |
    v
Recognized text
    |
    v
gTTS
    |
    v
Speaker
```

The monitor uses the image file's `modifiedTime` to detect a new capture.

The original prototype used polling. The cleaned implementation keeps that behavior because it is simple and matches the historical architecture.

## 3. Obstacle detection

```text
Ultrasonic sensor
       |
       v
Distance calculation
       |
       v
Distance < threshold?
       |
       +---- yes ---> Buzzer ON
       |
       +---- no ----> Buzzer OFF
```

The obstacle detector is independent from the Google Drive/OCR pipeline.

## Process model

The three components can run as separate processes on the Raspberry Pi:

```bash
python src/glasses/main.py
python src/processing/drive_monitor.py
python src/hardware/ultrasonic_sensor.py
```

This allows the microphone/camera, OCR processor, and obstacle detector to operate independently.

For a later deployment, these programs could be managed using `systemd` services so that they start automatically when the Raspberry Pi boots.

