import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(5,GPIO.OUT)     # BLUE
GPIO.setup(6,GPIO.OUT)     # RED
GPIO.setup(13,GPIO.OUT)    # GREEN

try:
    while(True):
        GPIO.output(13,0)
        GPIO.output(5,1)
        sleep(1)
        GPIO.output(5,0)
        GPIO.output(6,1)
        sleep(1)
        GPIO.output(6,0)
        GPIO.output(13,1)
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()


