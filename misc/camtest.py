#!/usr/bin/env python

from time import sleep, strftime
from datetime import datetime
from picamera import PiCamera, Color
import paramiko

camera = PiCamera()

class CamTest:
    try:
        def __init__(self):
            self.setstuff()

        def openconnect(self, rhost):
            self.client = paramiko.SSHClient()
            ourkey = paramiko.RSAKey.from_private_key_file('/home/pi/.ssh/id_rsa')
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(rhost, username='pi', pkey=ourkey)
            self.sftp = self.client.open_sftp()

        def closeconnect(self):
            self.client.close()
        
        def testremote(self, ourhost):
            try:
                # Moved openconnect to setstuff
                # self.openconnect(ourhost)
                print('Setting file:')
                f = self.sftp.open('/home/pi/Videos/remotetest.h264', 'w')
                print('Starting recording:')
                camera.start_recording(f, format='h264', quality=30)
                print('Recording started')
                camera.wait_recording(10)
                camera.stop_recording()
                self.closeconnect()
            except KeyboardInterrupt(): camera.stop_recording()
        
        def setstuff(self):
            camera.resolution = (400, 300)
            camera.framerate = 15
            camera.annotate_background = Color('black')
            camera.annotate_text_size = 20
            camera.rotation = 270
            self.openconnect('192.168.1.234')
        
        def cycleeffects(self):
            for effect in camera.IMAGE_EFFECTS:
            	camera.image_effect = effect
            	camera.annotate_text = "Effect: %s" % effect
            	sleep(5)
        
        def tryeffects(self):
            try:
            	while True:
            		cycleeffects()
            except KeyboardInterrupt: pass
        
        def andate(self):
            datestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
            camera.annotate_text = datestamp
        
        def keepdate(self, seconds):
            for y in range( 0, seconds // 10):
                andate()
                sleep(10)
        
        def testrecord(self, x):
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
                'testrecord(x):\n\tRecord for seconds (rounds to 10s)\n' + 
                'testremote(host):\n\tRecord over ssh on host\n\n' + \
                'Keyboard Interrupt cancels current operation.')
    
    except Exception:
        self.closeconnect()

def main():
    camtest = CamTest()
    camtest.testremote('192.168.1.234')

if __name__ == "__main__":
    camtest = CamTest()
    print('Variables set; running testremote():')
    camtest.testremote('192.168.1.234')
