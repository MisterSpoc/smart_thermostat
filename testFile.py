import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

GPIO.output(26, GPIO.HIGH)

try:
    while True:
        a=1
except:
    print("done")
    GPIO.cleanup()
