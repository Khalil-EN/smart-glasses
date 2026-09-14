import RPi.GPIO as GPIO
import time

# GPIO pin numbers for the ultrasonic sensor
TRIG_PIN = 14
ECHO_PIN = 15

BUZZER_PIN = 16

THRESHOLD_DISTANCE_CM = 20

def get_distance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 34300  # Speed of sound in cm/s
    distance = (pulse_duration * speed_of_sound) / 2
    return distance


GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

GPIO.output(TRIG_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)


try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")

        if distance < THRESHOLD_DISTANCE_CM:
            GPIO.output(BUZZER_PIN, GPIO.HIGH) 
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW) 

except KeyboardInterrupt:
    GPIO.cleanup()