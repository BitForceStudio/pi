from gpiozero import Motor, OutputDevice
from time     import sleep

import webiopi
import datetime

motor2 = Motor(6, 22)
motor2_enable = OutputDevice(17, initial_value=1)
motor3 = Motor(23, 16)
motor3_enable = OutputDevice(12, initial_value=1)

GPIO = webiopi.GPIO

ENABLE_M2 = 17 # GPIO pin using BCM numbering
ENABLE_M3 = 12

FORWARD_M2 = 6
FORWARD_M3 = 23

BACKWARD_M2 = 22
BACKWARD_M3 = 16

#HOUR_ON  = 8  # Turn Light ON at 08:00
#HOUR_OFF = 18 # Turn Light OFF at 18:00

# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used by the light to output
    GPIO.setFunction(ENABLE_M2, GPIO.OUT)
    GPIO.setFunction(ENABLE_M3, GPIO.OUT)

    # enable motor
    GPIO.digitalWrite(ENABLE_M2, GPIO.HIGH)
    GPIO.digitalWrite(ENABLE_M3, GPIO.HIGH)

    # set GPIO motor control
    GPIO.setFunction(FORWARD_M2,  GPIO.OUT)
    GPIO.setFunction(BACKWARD_M2, GPIO.OUT)

    GPIO.setFunction(FORWARD_M3,  GPIO.OUT)
    GPIO.setFunction(BACKWARD_M3, GPIO.OUT)

# loop function is repeatedly called by WebIOPi 
def loop():
    # retrieve current datetime
    now = datetime.datetime.now()

    # toggle light ON all days at the correct time
    if ((now.hour == HOUR_ON) and (now.minute == 0) and (now.second == 0)):
        if (GPIO.digitalRead(LIGHT) == GPIO.LOW):
            GPIO.digitalWrite(LIGHT, GPIO.HIGH)

    # toggle light OFF
    if ((now.hour == HOUR_OFF) and (now.minute == 0) and (now.second == 0)):
        if (GPIO.digitalRead(LIGHT) == GPIO.HIGH):
            GPIO.digitalWrite(LIGHT, GPIO.LOW)

    # gives CPU some time before looping again
    webiopi.sleep(1)

# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(LIGHT, GPIO.LOW)