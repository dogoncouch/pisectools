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
from picamera import PiCamera, Color



class LisardEyeCore:
    
    def __init__(self):
        syslog.openlog(facility=syslog.LOG_LOCAL2)

        self.pir_pin = 18
        io.setup(self.pir_pin, io.IN)
        
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 15
        self.camera.annotate_background = Color('black')
        self.camera.annotate_text_size = 10
        self.camera.framerate = 15
        
        self.videopath = '/home/pi/Videos'
        
        self.ismotion = False
        self.scount = 40



    def do_watch(self):

        while True:
            if io.input(self.pir_pin):
                if not self.ismotion:
                    syslog.syslog(syslog.LOG_INFO, 'PIR: Motion detected')
                    self.ismotion = True
                    self.scount = 40
                    self.datestamp = \
                            datetime.now().strftime('%Y-%m-%d-%H%M')
                    self.longdatestamp = \
                            datetime.now().strftime('%Y-%m-%d-%H%M%S')
                    self.filename = self.videopath + '/video-' + \
                            self.longdatestamp + '.h264'
                    self.camera.annotate_text = self.datestamp
                    self.camera.start_recording(self.filename)
                    syslog.syslog(syslog.LOG_INFO,
                            'Video: Started: ' + self.longdatestamp + \
                                    '.h264')
                else:
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
                    self.camera.stop_recording()
                    syslog.syslog(syslog.LOG_INFO,
                            'Video: Stopped: ' + self.longdatestamp + \
                                    '.h264')
                    self.ismotion = False
            sleep(0.5)



def main():
    sentry = LisardEyeCore()
    sentry.do_watch()

if __name__ == "__main__":
    sentry = LisardEyeCore()
    sentry.do_watch()
