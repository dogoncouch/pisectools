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
import RPi.GPIO as io
io.setmode(io.BCM)
import syslog
import argparse
import signal
from sys import exit
from picamera import PiCamera, Color



class LisardEyeCore:
    
    def __init__(self):
        """Initialize LISARD eye system"""

        # Open our log:
        syslog.openlog(facility=syslog.LOG_LOCAL2)

        # Clean shutdown:
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        # Basic settings:
        self.ismotion= False
        self.pir_pin = 18
        io.setup(self.pir_pin, io.IN)
        
        # CLI options:
        parser = argparse.ArgumentParser()
        parser.add_argument("--no-cam", action="store_true",
                help="disable camera support")
        parser.add_argument("--no-cam-date", action="store_true",
                help="disable datestamp in camera")
        parser.add_argument("--hd", action="store_true",
                help="enable 1080p video")
        parser.add_argument("--svga", action="store_true",
                help="enable svga video (800x600)")
        args = parser.parse_args()
        

        # Video recording mode setup:
        if not args.no-cam:
            self.camera = PiCamera()
            self.isrecording = False
            self.longdatestamp = ''
            self.videopath = '/home/pi/Videos'
        
            if args.hd:
                # self.camera.sensor_mode = 1
                self.camera.resolution = (1920, 1080)
                self.camera.framerate = 30
                if args.cam-date: self.camera.annotate_text_size = 25
            elif args.svga:
                # self.camera.sensor_mode = 5
                self.camera.resolution = (800, 600)
                self.camera.framerate = 30
                if args.cam-date: self.camera.annotate_text_size = 10
            else:
                self.camera.resolution = (400, 300)
                self.camera.framerate = 15
                if args.cam-date: self.camera.annotate_text_size = 8
                
            if args.cam-date:
                self.camera.annotate_background = Color('black')
                self.datestamp = ''
                self.scount = 40



    def sigterm_handler(self, signal, frame):
        """Exits cleanly in the event of shutdown/sigterm"""
        syslog.syslog(syslog.LOG_NOTICE, 'Received SIGTERM. Exiting')
                    syslog.syslog(syslog.LOG_INFO,
                            'Video: Stopped: ' + self.longdatestamp + \
                                    '.h264')
        self.camera.stop_recording()
        exit(0)



    def do_run(self):
        """Runs the watch job"""
        try:
            self.do_watch()
        except KeyboardInterrupt:
            syslog.syslog(syslog.LOG_NOTICE,
                    'Received KeyboardInterrupt. Exiting')
            syslog.syslog(syslog.LOG_INFO,
                    'Video: Stopped: ' + self.longdatestamp + \
                            '.h264')
            self.camera.stop_recording
            exit(0)
    


    def do_watch(self):
        """Monitors motion sensor and records video (optional)"""
        while True:
            if io.input(self.pir_pin):
                if not self.ismotion:
                    syslog.syslog(syslog.LOG_INFO, 'PIR: Motion detected')
                    self.ismotion = True
                    if not args.no-cam:
                        if not args.no-cam-date:
                            self.scount = 40
                            self.datestamp = \
                                    datetime.now().strftime('%Y-%m-%d-%H%M')
                            self.camera.annotate_text = self.datestamp
                        self.longdatestamp = \
                                datetime.now().strftime('%Y-%m-%d-%H%M%S')
                        self.filename = self.videopath + '/video-' + \
                                self.longdatestamp + '.h264'
                        self.camera.start_recording(self.filename)
                        syslog.syslog(syslog.LOG_INFO,
                                'Video: Started: ' + self.longdatestamp + \
                                        '.h264')
                else:
                    if not args.no-cam-date:
                        if self.scount == 0:
                            self.datestamp = \
                                    datetime.now().strftime('%Y-%m-%d-%H%M')
                            self.camera.annotate_text = self.datestamp
                            self.scount = 40
                        else:
                            self.scount = self.scount - 1
            else:
                if self.ismotion:
                    syslog.syslog(syslog.LOG_INFO, 'PIR: Motion stopped')
                    if not args.no-cam:
                        self.camera.stop_recording()
                        syslog.syslog(syslog.LOG_INFO,
                                'Video: Stopped: ' + self.longdatestamp + \
                                        '.h264')
                    self.ismotion = False
            sleep(0.5)



def main():
    sentry = LisardEyeCore()
    sentry.do_run()

if __name__ == "__main__":
    sentry = LisardEyeCore()
    sentry.do_run()
