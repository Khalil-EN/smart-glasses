import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import settings


try:
    import RPi.GPIO as GPIO
except ImportError as exc:
    raise RuntimeError(
        "RPi.GPIO is required to run the ultrasonic sensor on a Raspberry Pi."
    ) from exc


def get_distance(trig_pin: int, echo_pin: int, timeout: float = 0.1) -> float | None:
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    deadline = time.monotonic() + timeout
    while GPIO.input(echo_pin) == 0:
        if time.monotonic() >= deadline:
            return None
    pulse_start = time.monotonic()

    deadline = time.monotonic() + timeout
    while GPIO.input(echo_pin) == 1:
        if time.monotonic() >= deadline:
            return None
    pulse_end = time.monotonic()

    pulse_duration = pulse_end - pulse_start
    return (pulse_duration * 34300) / 2


def main() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings.TRIG_PIN, GPIO.OUT)
    GPIO.setup(settings.ECHO_PIN, GPIO.IN)
    GPIO.setup(settings.BUZZER_PIN, GPIO.OUT)

    GPIO.output(settings.TRIG_PIN, GPIO.LOW)
    GPIO.output(settings.BUZZER_PIN, GPIO.LOW)

    print("Ultrasonic obstacle detector started.")

    try:
        while True:
            distance = get_distance(settings.TRIG_PIN, settings.ECHO_PIN)

            if distance is None:
                GPIO.output(settings.BUZZER_PIN, GPIO.LOW)
                print("Distance measurement timed out.")
            else:
                print(f"Distance: {distance:.2f} cm")
                GPIO.output(
                    settings.BUZZER_PIN,
                    GPIO.HIGH if distance < settings.THRESHOLD_DISTANCE_CM else GPIO.LOW,
                )

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopping ultrasonic detector.")
    finally:
        GPIO.output(settings.BUZZER_PIN, GPIO.LOW)
        GPIO.cleanup()


if __name__ == "__main__":
    main()
