# Picon Zero Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# To check wiring is correct ensure the order of movement as above is correct

import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

speed = 100

pz.init()


def moveforward():
    try:
        pz.forward(speed)
        time.sleep(0.1)
        pz.stop()
    except: KeyboardInterrupt:
        print "quit"


# main loop
try:
    while True:
        keyp = readkey()
        if keyp == 'w' or ord(keyp) == 16:
            pz.forward(speed)
            print 'Forward', speed
        elif keyp == 'z' or ord(keyp) == 17:
            pz.reverse(speed)
            print 'Reverse', speed
        elif keyp == 's' or ord(keyp) == 18:
            pz.spinRight(speed)
            print 'Spin Right', speed
        elif keyp == 'a' or ord(keyp) == 19:
            pz.spinLeft(speed)
            print 'Spin Left', speed
        elif keyp == '.' or keyp == '>':
            speed = min(100, speed+10)
            print 'Speed+', speed
        elif keyp == ',' or keyp == '<':
            speed = max (0, speed-10)
            print 'Speed-', speed
        elif keyp == ' ':
            pz.stop()
            print 'Stop'
        elif ord(keyp) == 3:
            break
        time.sleep(0.5)
        pz.stop()

except KeyboardInterrupt:
    print

finally:
    pz.cleanup()
    
