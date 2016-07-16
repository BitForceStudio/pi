
import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room

import piconzero as pz, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys,tty,termios

speed = 100
# Define which pins are the servos
pan = 0
tilt = 1
step = 5
pz.init()

# Set output mode to Servo
pz.setOutputConfig(pan, 2)
pz.setOutputConfig(tilt, 2)

# Centre all servos
panVal = 90
tiltVal = 90

pz.setOutput (pan, panVal)
pz.setOutput (tilt, tiltVal)

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    isCarcontrol = False
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        if prefix == "control":
            log.debug('car control mode')
            isCarcontrol = True
        elif prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(label=label)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('ws room does not exist label=%s', label)
        return

    log.debug('chat connect room=%s client=%s:%s', 
        room.label, message['client'][0], message['client'][1])
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    if isCarcontrol:
        Group('control-'+label, channel_layer=message.channel_layer).add(message.reply_channel)
    else:
        Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.label

@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    if room.label=="remotecarcontrol":
        log.debug('car control mode')
        data=''
        try:
            #data = message['text']
            data = json.loads(message['text'])
        except ValueError:
            log.debug("ws message isn't json text=%s", data)
            return

  #      movex(data['x'])
        movey(data['y'])

        log.debug("move x:%d  y:%d", data['x'],data['y'])
            # See above for the note about Group
        Group('control-'+label, channel_layer=message.channel_layer).send({'text': data})
    else:
        try:
            data = json.loads(message['text'])
        except ValueError:
            log.debug("ws message isn't json text=%s", text)
            return
        
        if set(data.keys()) != set(('handle', 'message')):
            log.debug("ws message unexpected format data=%s", data)
            return

        if data:
            log.debug('chat message room=%s handle=%s message=%s', 
                room.label, data['handle'], data['message'])
            m = room.messages.create(**data)

            # See above for the note about Group
            Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        if room.label=="remotecarcontrol":
            pz.cleanup()
            Group('control-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
        else:
            Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass

def moverightturn():
    global pz,speed
    try:
        pz.forward(speed)
        time.sleep(0.05)
	pz.spinRight(speed)
	time.sleep(0.05)
	pz.forward(speed)
	time.sleep(0.05)
        pz.stop()
    except KeyboardInterrupt:
        print "quit"

def moveleftturn():
    global pz,speed
    try:
        pz.reverse(speed)
        time.sleep(0.05)
        pz.spinLeft(speed)
        time.sleep(0.05)
        pz.reverse(speed)
        time.sleep(0.05)
        pz.spinLeft(speed)
        time.sleep(0.1)
        pz.stop()
    except KeyboardInterrupt:
        print "quit"

def movebackward():
    global pz,speed
    try:
        pz.spinRight(speed)
        time.sleep(0.05)
        pz.stop()
    except KeyboardInterrupt:
        print "quit"

def moveforward():
    global pz,speed
    try:
        pz.spinLeft(speed)
        time.sleep(0.1)
        pz.stop()
    except KeyboardInterrupt:
        print "quit"

def moveup():
    global panVal,step,pz,pan
    try:
        panVal = max (65, panVal + step)
        pz.setOutput (pan, panVal)
    except KeyboardInterrupt:
        print "quit"

def movedown():
    global panVal,step,pz,pan
    try:
        panVal = min (160, panVal - step)
        pz.setOutput (pan, panVal)
    except KeyboardInterrupt:
        print "quit"

def moveright():
    global tiltVal,step,pz,tilt
    try:
        tiltVal = max (20, tiltVal - step)
        pz.setOutput (tilt, tiltVal)
    except KeyboardInterrupt:
        print "quit"

def moveleft():
    global tiltVal,step,pz,tilt
    try:
        tiltVal = min (160, tiltVal + step)
        pz.setOutput (tilt, tiltVal)
    except KeyboardInterrupt:
        print "quit"

def movex(x):
    global tiltVal,pz,tilt
    try:
        tiltVal = min (160, tiltVal+x)
        tiltVal = max (20,  tiltVal+x)
        pz.setOutput (tilt, panVal)
    except KeyboardInterrupt:
        print "quit"


def movey(y):
    global panVal,pz,pan
    try:
        panVal = max (40, y)
        panVal = min (160, y)
        pz.setOutput (pan, panVal)
    except KeyboardInterrupt:
        print "quit"




