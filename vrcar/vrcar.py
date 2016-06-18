from gpiozero import Motor, OutputDevice
from time import sleep

motor2 = Motor(6, 22)
motor2_enable = OutputDevice(17, initial_value=1)
motor3 = Motor(23, 16)
motor3_enable = OutputDevice(12, initial_value=1)

def left_turn():
    motor3.forward()
    motor2.backward()
    sleep(2)

def right_turn():
    motor3.backward()
    motor2.forward()
    sleep(2)

if __name__ == '__main__':
    cmd=''
    while cmd is not 'exit':
        if cmd=='w':
            motor2.forward() # full speed forwards
            motor3.forward() # full speed forwards
            sleep(2)
        elif cmd=='s':
            motor2.backward() # full speed backwards
            motor3.backward() # full speed backwards
            sleep(2)
        elif cmd=='a':
            left_turn()
        elif cmd=='d':
            right_turn()
        elif cmd=='e':
            break
