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
from lisard import cam
# import lisard
# from picamera import PiCamera, Color



class LisardEyeCore:
    
    def __init__(self):
        """Initialize LISARD eye system"""

        # Open our log:
        syslog.openlog(facility=syslog.LOG_LOCAL2)

        # Clean shutdown:
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        # Basic settings:
        self.is_motion = False
        self.is_remote = False
        self.pir_pin = 18
        io.setup(self.pir_pin, io.IN)
        
        # CLI options:
        parser = argparse.ArgumentParser()
        parser.add_argument("--remote", action="store",
                help="set remote host for video files")
        parser.add_argument("--nocam", action="store_true",
                help="disable camera support")
        parser.add_argument("--nocamdate", action="store_true",
                help="disable datestamp in camera")
        parser.add_argument("--fhd", action="store_true",
                help="enable 1080p video")
        parser.add_argument("--hd", action="store_true",
                help="enable 720p video")
        parser.add_argument("--svga", action="store_true",
                help="enable svga video (800x600)")
        parser.add_argument("--vga", action="store_true",
                help="enable vga video (640x480)")
        parser.add_argument("--ld", action="store_true",
                help="enable low def video (400x300)")
        self.args = parser.parse_args()
        

        # Video recording mode setup:
        if not self.args.nocam:
            self.cam = cam.LisardCam()
            self.is_recording = False
            self.long_date_stamp = ''
            self.video_path = '/home/pi/Videos' # To Do: get from args

            # Set up remote recording
            if self.args.remote:
                self.is_remote = True
                self.cam.open_connect(remote[0])
        
            # Set video quality:
            if self.args.fhd:
                self.cam.set_res('fhd')
            elif self.args.hd:
                self.cam.set_res('hd')
            elif self.args.svga:
                self.cam.set_res('svga')
            elif self.args.vga:
                self.cam.set_res('vga')
            else:
                self.cam.set_res('ld')

            if not self.args.nocamdate:
                self.cam.annotate = True



    def sigterm_handler(self, signal, frame):
        """Exits cleanly in the event of shutdown/sigterm"""
        syslog.syslog(syslog.LOG_NOTICE, 'Received SIGTERM. Exiting')
        if self.is_recording:
            self.cam.stop_cam()
            syslog.syslog(syslog.LOG_INFO,'Video: Stopped: ' + \
                    self.long_date_stamp + '.h264')
            if self.is_remote:
                try: self.cam.close_connect()
                except Exception: pass
        exit(0)



    def do_run(self):
        """Runs the watch job"""
        try:
            self.do_watch()
        except KeyboardInterrupt:
            syslog.syslog(syslog.LOG_NOTICE,
                    'Received KeyboardInterrupt. Exiting')
            if self.is_recording:
                self.cam.stop_cam()
                syslog.syslog(syslog.LOG_INFO,
                        'Video: Stopped: ' + self.long_date_stamp + \
                                '.h264')
            if self.is_remote:
                try: self.cam.close_connect()
                except Exception: pass
            exit(0)
    


    def do_watch(self):
        """Monitors motion sensor and records video (optional)"""
        while True:
            if io.input(self.pir_pin):
                if not self.is_motion:
                    # Start recording:
                    syslog.syslog(syslog.LOG_INFO, 'PIR: Motion detected')
                    self.is_motion = True
                    hscount = 1200
                    if not self.args.nocam:
                        self.long_date_stamp = \
                                datetime.now().strftime('%Y-%m-%d-%H%M%S')
                        self.cam.start_cam(self.long_date_stamp + '.h264')
                        syslog.syslog(syslog.LOG_INFO,
                                'Video: Started: ' + self.long_date_stamp + \
                                        '.h264')
                else:
                    # Split recording every 20 minutes:
                    if hscount == 0:
                        self.long_date_stamp = \
                                datetime.now().strftime('%Y-%m-%d-%H%M%S')
                        self.cam.camera.split_recording(self.long_date_stamp + \
                                '.h264')

                        syslog.syslog(syslog.LOG_INFO,
                                'Video: Split: ' + self.long_date_stamp + \
                                        '.h264')
                        hscount = 1200
                    else:
                        hscount = hscount - 1

            else:
                if self.is_motion:
                    # Stop recording:
                    syslog.syslog(syslog.LOG_INFO, 'PIR: Motion stopped')
                    if not self.args.nocam:
                        self.cam.stop_cam()
                        syslog.syslog(syslog.LOG_INFO,
                                'Video: Stopped: ' + self.long_date_stamp + \
                                        '.h264')
                    self.is_motion = False
            sleep(0.5)



def main():
    sentry = LisardEyeCore()
    sentry.do_run()

if __name__ == "__main__":
    sentry = LisardEyeCore()
    sentry.do_run()
