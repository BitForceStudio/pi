from gpiozero import Motor, OutputDevice
from time import sleep

motor2 = Motor(6, 22)
motor2_enable = OutputDevice(17, initial_value=1)
motor3 = Motor(23, 16)
motor3_enable = OutputDevice(12, initial_value=1)
i=0
while i<10:
    motor2.forward() # full speed forwards
    motor3.forward() # full speed forwards

    sleep(3)

    motor2.backward() # full speed backwards
    motor3.backward() # full speed backwards

    sleep(3)

    motor2.forward() # stop the motor
    motor3.stop() # stop the motor

    sleep(1) 

    motor3.forward()
    motor2.stop()

    sleep(1)

    i=i+1
