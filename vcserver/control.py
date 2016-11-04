# python control script
import sys, json
import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import tty,termios

speed = 100
# Define which pins are the servos
pan = 0
tilt = 1
step = 5
pz.init()

# simple JSON echo script
for line in sys.stdin:
  command = json.dumps(json.loads(line))
  