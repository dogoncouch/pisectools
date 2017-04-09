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
from sys import exit
import signal
import subprocess
import argparse
import RPi.GPIO as io
io.setmode(io.BCM)
from picamera import PiCamera, Color



class ModesCore:
    
    def __init__(self):

        # Clean shutdown:
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        
        # CLI options:
        parser = argparse.ArgumentParser()
        parser.add_argument("--no-cam", action="store_true",
                help="disable camera support")
        parser.add_argument("--cam-date", action="store_true",
                help="enable datestamp in camera")
        parser.add_argument("--hd", action="store_true",
                help="enable 1080p video")
        parser.add_argument("--ld", action="store_true",
                help="enable 400x300 video")
        parser.add_argument("--no-rec-stop", action="store_true",
                help="keep recording when jumper is removed")
        args = parser.parse_args()
        
        
        # Video recording mode setup:
        if not args.no-cam:
            self.cam_pin = 10
            io.setup(self.cam_pin, io.IN)
            self.camera = PiCamera()
            self.isrecording = False
            self.longdatestamp = ''
            self.videopath = '/home/pi/Videos'
        
            if args.hd:
                # self.camera.sensor_mode = 1
                self.camera.resolution = (1920, 1080)
                self.camera.framerate = 30
                if args.cam-date: self.camera.annotate_text_size = 25
            elif args.ld:
                self.camera.resolution = (400, 300)
                self.camera.framerate = 15
                if args.cam-date: self.camera.annotate_text_size = 8
            else:
                # self.camera.sensor_mode = 5
                self.camera.resolution = (800, 600)
                self.camera.framerate = 30
                if args.cam-date: self.camera.annotate_text_size = 10
                
            if args.cam-date:
                self.camera.annotate_background = Color('black')
                self.datestamp = ''
                self.scount = 40

        # Other pin 10 script setup:
        else: self.other10 = False

        # Radio mode setup:
        self.radio_pin = 22
        io.setup(self.radio_pin, io.IN)
        self.radiostream = 'http://amber.streamguys.com:4860'
        self.isradio = False
        
        # Wifi mode setup:
        self.wifi_pin = 27
        io.setup(self.wifi_pin, io.IN)
        
        # Stop mode setup:
        self.stop_pin = 2
        io.setup(self.stop_pin, io.IN)
        
        # Shutdown mode setup:
        self.shutdown_pin = 24
        io.setup(self.shutdown_pin, io.IN)



    def do_run(self):
        try:
            self.do_modes()
        except KeyboardInterrupt:
            self.do_stop()
            exit(0)
    
    
    
    def do_stop(self):
        if not args.no-cam:
            if self.isrecording:
                self.camera.stop_recording()
                self.isrecording = False
                if args.cam-date: self.scount = 40
        elif self.other10:
            subprocess.Popen(['/usr/bin/killall', 'other10.sh'])
            self.other10 = False
        if self.isradio:
            subprocess.Popen(['/usr/bin/killall', 'mpg123'])
            self.isradio = False
        if self.iswifi:
            subprocess.Popen(['/usr/bin/killall', 'wifi.sh'])
            self.iswifi = False



    def sigterm_handler(self, signal, frame):
        self.do_stop()
        exit(0)

    

    def do_modes(self):

        while True:
            
            # Video recording mode:
            if not args.no-cam:
                if io.input(self.cam_pin):
                    if not self.isrecording:
                        if args.cam-date:
                            self.datestamp = \
                                datetime.now().strftime('%Y-%m-%d-%H%M')
                            self.camera.annotate_text = self.datestamp
                            self.scount = 40
                        self.longdatestamp = \
                                datetime.now().strftime('%Y-%m-%d-%H%M%S')
                        self.filename = self.videopath + '/video-' + \
                                self.longdatestamp + '.h264'
                        self.camera.start_recording(self.filename)
                        self.isrecording = True
                    else:
                        if args.cam-date:
                            if self.scount == 0:
                                self.datestamp = \
                                        datetime.now().strftime('%Y-%m-%d-%H%M')
                                self.camera.annotate_text = self.datestamp
                                self.scount = 40
                            else:
                                self.scount = self.scount - 1
                else:
                    if args.no-rec-stop:
                        if self.isrecording and args.cam-date:
                            # if args.cam-date:
                            if self.scount == 0:
                                self.datestamp = \
                                        datetime.now().strftime('%Y-%m-%d-%H%M')
                                self.camera.annotate_text = self.datestamp
                                self.scount = 40
                            else:
                                self.scount = self.scount - 1
                    else:
                        self.camera.stop_recording()
                        self.isrecording = False
                    

            else:
                subprocess.Popen(['/home/pi/bin/other10.sh'])
                self.other10 = True
                    


            # Radio mode:
            if io.input(self.radio_pin):
                if not self.isradio:
                    subprocess.Popen(['/usr/bin/amixer', 'cset', 'numid',
                        '3', '1'])
                    subprocess.Popen(['/usr/bin/mpg123 ', self.radiostream])
                    self.isradio = True


            # Wifi mode:
            if io.input(self.wifi_pin):
                if not self.iswifi:
                    subprocess.Popen(['/home/pi/bin/wifi.sh'])
                    self.iswifi = True


            # Stop mode:
            if io.input(self.stop_pin):
                self.do_stop()


            # Shutdown mode:
            if io.input(self.shutdown_pin):
                self.do_stop()
                subprocess.Popen(['shutdown', '-h', 'now'])


            sleep(0.5)



def main():
    sentry = ModesCore()
    sentry.do_run()

if __name__ == "__main__":
    sentry = ModesCore()
    sentry.do_run()
