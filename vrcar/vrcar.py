from gpiozero import Motor, OutputDevice
from time import sleep

motor2 = Motor(6, 22)
motor2_enable = OutputDevice(17, initial_value=1)
motor3 = Motor(23, 16)
motor3_enable = OutputDevice(12, initial_value=1)

turn_time=0.95

def forward():
    motor2.forward()
    motor3.forward()
    sleep(1.5)

def backward():
    motor3.backward()
    motor2.backward()
    sleep(1.5)

def left_turn():
    motor3.forward()
    motor2.backward()
    sleep(turn_time)

def right_turn():
    motor3.backward()
    motor2.forward()
    sleep(turn_time)

def eight():
    forward()
    right_turn()
    forward()
    right_turn()
    forward()
    right_turn()
    forward()
    backward()
    left_turn()
    backward()
    left_turn()
    backward()
    left_turn()
    backward()    
# 
if __name__ == '__main__':
    cmd=''
    while cmd is not 'e':
        cmd=raw_input('Cmd:')
        if cmd=='w':
            print "forword 2 sec"
            motor2.forward() # full speed forwards
            motor3.forward() # full speed forwards
            sleep(2)          
        elif cmd=='s':
            print "backword 2 sec"
            motor2.backward() # full speed backwards
            motor3.backward() # full speed backwards
            sleep(2)
        elif cmd=='a':
            print "left turn"
            left_turn()
        elif cmd=='d':
            print "right turn"
            right_turn()
        elif cmd=='8':
            print "run 8"
            eight()
        elif cmd=='e':
            break
        motor2.stop()
        motor3.stop()

