import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, OUTPUT)

GPIO.output(17, GPIO.LOW)
GPIO.cleanup()
