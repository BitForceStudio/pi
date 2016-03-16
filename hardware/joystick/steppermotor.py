import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(16,GPIO.OUT)     # in1
GPIO.setup(19,GPIO.OUT)     # in2
GPIO.setup(20,GPIO.OUT)     # in3
GPIO.setup(21,GPIO.OUT)     # in4

try:
    while(True):
        sleep(0.5)
        GPIO.output(16,1)
        GPIO.output(19,0)
        GPIO.output(20,0)
        GPIO.output(21,0)
        sleep(0.5)
        GPIO.output(16,0)
        GPIO.output(19,1)
        GPIO.output(20,0)
        GPIO.output(21,0)
        sleep(0.5)
        GPIO.output(16,0)
        GPIO.output(19,0)
        GPIO.output(20,1)
        GPIO.output(21,0)
        sleep(0.5)
        GPIO.output(16,0)
        GPIO.output(19,0)
        GPIO.output(20,0)
        GPIO.output(21,1)
except KeyboardInterrupt:
    GPIO.cleanup()
