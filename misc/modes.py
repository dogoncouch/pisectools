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
import subprocess
import RPi.GPIO as io
io.setmode(io.BCM)
from picamera import PiCamera, Color



class ModesCore:
    
    def __init__(self):

        # Video recording mode setup:
        self.cam_pin = 24 # To Do: change this?
        io.setup(self.cam_pin, io.IN)
        self.camera = PiCamera()
        self.camera.resolution = (800, 600)
        self.camera.framerate = 30
        self.camera.annotate_background = Color('black')
        self.camera.annotate_text_size = 10
        
        self.videopath = '/home/pi/Videos'
        self.isrecording = False
        self.scount = 40

        # Radio mode setup:
        self.radio_pin = 22# To Do
        io.setup(self.radio_pin, io.IN)
        self.radiostream = 'http://amber.streamguys.com:4860'
        self.isradio = False
        
        # Wifi mode setup:
        self.wifi_pin = 2# To Do: check
        io.setup(self.wifi_pin, io.IN)
        
        # Shutdown mode setup:
        self.shutdown_pin = 10 # To Do: check
        io.setup(self.shutdown_pin, io.IN)



    def do_modes(self):

        while True:
            
            # Video recording mode:
            if io.input(self.cam_pin):
                if not self.isrecording:
                    self.datestamp = \
                            datetime.now().strftime('%Y-%m-%d-%H%M')
                    self.longdatestamp = \
                            datetime.now().strftime('%Y-%m-%d-%H%M%S')
                    self.filename = self.videopath + '/video-' + \
                            self.longdatestamp + '.h264'
                    self.camera.annotate_text = self.datestamp
                    self.camera.start_recording(self.filename)
                    self.isrecording = True
                    self.scount = 40
                else:
                    if self.scount == 0:
                        self.datestamp = \
                                datetime.now().strftime('%Y-%m-%d-%H%M')
                        self.camera.annotate_text = self.datestamp
                        self.scount = 40
                    else:
                        self.scount = self.scount - 1
            else:
                if self.isrecording:
                    self.camera.stop_recording()
                    self.isrecording = False


            # Radio mode:
            if io.input(self.radio_pin):
                if not self.isradio:
                    subprocess.Popen('amixer cset numid 3 1')
                    subprocess.Popen('mpg123 ' + self.radiostream)
                    self.isradio = True
            else:
                if self.isradio:
                    subprocess.Popen('killall mpg123')
                    subprocess.Popen('amixer cset numid=3 0')
                    self.isradio = False


            # Wifi mode:
            if io.input(self.wifi_pin):
                if not self.iswifi:
                    subprocess.popen('/home/pi/bin/wifi.sh')
                    self.iswifi = True
            else:
                if self.iswifi:
                    subprocess.popen('killall wifi.sh')
                    self.iswifi = False


            # Shutdown mode:
            if io.input(self.shutdown_pin):
                self.camera.stop_recording()
                subprocess.Popen('shutdown -h now')


            sleep(0.5)



def main():
    sentry = ModesCore()
    sentry.do_modes()

if __name__ == "__main__":
    sentry = ModesCore()
    sentry.do_modes()
