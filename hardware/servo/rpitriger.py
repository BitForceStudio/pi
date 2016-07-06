import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
pwmon = GPIO.PWM(5, 100)
pwmoff = GPIO.PWM(6, 100)
pwmon.start(1)
pwmoff.start(1)
up  =1.0
down=11.0

while True:
    qclick = raw_input("do you want to turn on/off(y/n): ")
    if qclick == "y":
        pwmon.ChangeDutyCycle(down)
        sleep(0.4)
        pwmon.ChangeDutyCycle(up)
    elif qclick == "n":
        pwmoff.ChangeDutyCycle(down)
        sleep(0.4)
        pwmoff.ChangeDutyCycle(up)
    else:
        pwmon.stop()
        pwmoff.stop()
        GPIO.cleanup()
        break

