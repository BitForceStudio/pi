import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
pwm = GPIO.PWM(21, 100)
pwm.start(5)


while True:
    angle = raw_input("input angle[0~100(%)]: ")
    if angle == "exit":
        pwm.stop()
        GPIO.cleanup()
        break
    angle = float(angle)
    if angle > 100:
        print "please input right angle"
    else:
        print angle
        duty = float(angle)
        pwm.ChangeDutyCycle(duty)
