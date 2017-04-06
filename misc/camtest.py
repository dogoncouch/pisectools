#!/usr/bin/env python

from time import sleep, strftime
from datetime import datetime
from picamera import PiCamera, Color

camera = PiCamera()

def setstuff():
    camera.resolution = (640, 480)
    camera.framerate = 15
    camera.annotate_background = Color('black')
    camera.annotate_text_size = 20

def cycleeffects():
    for effect in camera.IMAGE_EFFECTS:
    	camera.image_effect = effect
    	camera.annotate_text = "Effect: %s" % effect
    	sleep(5)

def tryeffects():
    try:
    	while True:
    		cycleeffects()
    except KeyboardInterrupt: pass

def andate():
    datestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
    camera.annotate_text = datestamp

def keepdate(seconds):
    for y in range( 0, seconds // 10):
        andate()
        sleep(10)

def testrecord(x):
    try:
        testimate = x // 10
        ourdatestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        andate()
        camera.start_recording(ourdatestamp + '.h264')
        keepdate(x)
        camera.stop_recording()
        del(ourdatestamp)
    except KeyboardInterrupt(): camera.stop_recording()

def showhelp():
    print('Functions:\n\nkeepdate():\n\tAnnotate timestamp\n' + \
        'setstuff():\n\tSet a lower resolution and frame rate\n' + \
        'tryeffects():\n\tCycle through effects\n' + \
        'testrecord(x):\n\tRecord for seconds (rounds to 10s)\n\n' + \
        'Keyboard Interrupt cancels current operation.')
