import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(16,GPIO.IN)     # X
GPIO.setup(20,GPIO.IN)     # Y
GPIO.setup(21,GPIO.IN)     # SW

GPIO.setup(5,GPIO.OUT)     # BLUE
GPIO.setup(6,GPIO.OUT)     # RED
GPIO.setup(13,GPIO.OUT)    # GREEN

try:
    while(True):
        GPIO.output(5 ,1-GPIO.input(16))
        GPIO.output(6 ,1-GPIO.input(20))
        GPIO.output(13,1-GPIO.input(21))
        print GPIO.input(16)
        print GPIO.input(20)
        print GPIO.input(21)
        sleep(3)
        print '----------'
except KeyboardInterrupt:
    GPIO.cleanup()
