#!/usr/bin/env python

#_MIT License
#_
#_Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
#_
#_Permission is hereby granted, free of charge, to any person obtaining a copy
#_of this software and associated documentation files (the "Software"), to deal
#_in the Software without restriction, including without limitation the rights
#_to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#_copies of the Software, and to permit persons to whom the Software is
#_furnished to do so, subject to the following conditions:
#_
#_The above copyright notice and this permission notice shall be included in all
#_copies or substantial portions of the Software.
#_
#_THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#_IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#_FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#_AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#_LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#_OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#_SOFTWARE.

from time import sleep, strftime
from datetime import datetime
from picamera import PiCamera, Color
import paramiko


class CamTest:
    try:
        def __init__(self):
            self.camera = PiCamera()
            self.camera.resolution = (800, 600)
            self.camera.framerate = 15
            self.camera.annotate_background = Color('black')
            self.camera.annotate_text_size = 20
            self.camera.rotation = 270
            # self.openconnect('192.168.1.234')

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
                self.camera.start_recording(f, format='h264', quality=30)
                print('Recording started')
                self.camera.wait_recording(10)
                self.camera.stop_recording()
                # self.closeconnect()
            except KeyboardInterrupt(): camera.stop_recording()
        
        def cycleeffects(self):
            for effect in self.camera.IMAGE_EFFECTS:
            	self.camera.image_effect = effect
            	self.camera.annotate_text = "Effect: %s" % effect
            	sleep(5)
        
        def tryeffects(self):
            try:
            	while True:
            		self.cycleeffects()
            except KeyboardInterrupt: pass
        
        def andate(self):
            datestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
            self.camera.annotate_text = datestamp
        
        def keepdate(self, seconds):
            for y in range( 0, seconds // 10):
                self.andate()
                sleep(10)
        
        def testrecord(self, x):
            try:
                testimate = x // 10
                ourdatestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
                andate()
                self.camera.start_recording(ourdatestamp + '.h264')
                keepdate(x)
                self.camera.stop_recording()
                del(ourdatestamp)
            except KeyboardInterrupt(): camera.stop_recording()
        
        def showhelp(self):
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
    camtest.testremote('192.168.1.234')
