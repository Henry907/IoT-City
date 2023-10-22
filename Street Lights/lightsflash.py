import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, OUTPUT)

i = 0

while (i<5):
  GPIO.output(17, GPIO.HIGH)
  time.sleep(.5)
  GPIO.output(17, GPIO.LOW)
  time.sleep(.5)
