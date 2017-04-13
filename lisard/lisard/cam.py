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
import threading


class LisardCam:
    
    def __init__(self):
        """Initialize a LisardCam pi camera object"""
        self.camera = PiCamera()
        self.set_res('fhd')
        self.annotate = True
        self.camera.annotate_background = Color('black')
        self.camera.rotation = 270
        self.is_recording = False
        self.is_remote = False
        self.sftp = None
        self.key_file = '/home/pi/.ssh/id_rsa'
        self.output_dir = '/home/pi/Videos'

    
    
    def set_res(self, res='fhd'):
        """Set pi camera resolution mode"""
        if res == 'fhd':
            self.camera.resolution = (1920, 1080)
            self.camera.framerate = 30
            self.camera.annotate_text_size = 30
        elif res == 'hd':
            self.camera.resolution = (1280, 720)
            self.camera.framerate = 30
            self.camera.annotate_text_size = 20
        elif res == 'svga':
            self.camera.resolution = (800, 600)
            self.camera.framerate = 30
            self.camera.annotate_text_size = 10
        elif res == 'vga':
            self.camera.resolution = (640, 480)
            self.camera.framerate = 30
            self.camera.annotate_text_size = 10
        elif res == 'ld':
            self.camera.resolution = (400, 300)
            self.camera.framerate = 15
            self.camera.annotate_text_size = 8
        else:
            raise ValueError('Unrecognized resolution input')

    
    
    def open_connect(self, rhost, user='pi', trustkeys=False):
        """Open an sftp connection for recording"""
        self.is_remote = True
        self.client = paramiko.SSHClient()
        ourkey = paramiko.RSAKey.from_private_key_file(self.key_file)
        self.client.load_system_host_keys()
        if trustkeys:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(rhost, username=user, pkey=ourkey)
        self.sftp = self.client.open_sftp()

    def close_connect(self):
        """Close sftp connection"""
        self.client.close()
        self.is_remote = False
    


    def time_stamp(self):
        """Keep pi camera timestamp updated"""
        while self.is_recording:
            datestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
            self.camera.annotate_text = datestamp
            sleep(5)
    
    
    
    def start_cam(self, filename):
        """Start recording"""
        # ourdatestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        fullname = self.output_dir + '/' + filename
        self.is_recording = True
        if self.is_remote == True:
            f = self.sftp.open(fullname, 'w')
        else:
            f = fullname
        if self.annotate == True:
            tstamp = threading.Thread(name='background',
                    target=self.time_stamp)
            tstamp.start()
        self.camera.start_recording(f)

    def stop_cam(self):
        """Stop recording"""
        self.is_recording = False
        self.camera.stop_recording()
    
    
    
    def cycle_effects(self):
        """Cycle through available pi camera effects"""
        try:
            while True:
                for effect in self.camera.IMAGE_EFFECTS:
        	        self.camera.image_effect = effect
            	self.camera.annotate_text = "Effect: %s" % effect
            	sleep(5)
        except Exception: pass
    
    

def main():
    cam = LisardCam()
    cam.start_cam()

if __name__ == "__main__":
    cam = LisardCam()
    cam.start_cam()
