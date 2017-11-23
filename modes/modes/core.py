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
# from picamera import PiCamera, Color



class ModesCore:
    
    def __init__(self):

        # Clean shutdown:
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        
        # CLI options:
        parser = argparse.ArgumentParser()
        parser.add_argument("--nocam", action="store_true",
                help="disable camera support")
        parser.add_argument("--camdate", action="store_true",
                help="enable datestamp in camera")
        parser.add_argument("--rotation", action="store",
                help="set camera rotation")
        parser.add_argument("--fhd", action="store_true",
                help="enable 1080p video")
        parser.add_argument("--hd", action="store_true",
                help="enable 720p video")
        parser.add_argument("--svga", action="store_true",
                help="enable svga video (800x600)")
        parser.add_argument("--vga", action="store_true",
                help="enable vga video (640x480)")
        parser.add_argument("--ld", action="store_true",
                help="enable low def video (400x300, 15fps)")
        parser.add_argument("--norecstop", action="store_true",
                help="keep recording when jumper is removed")
        parser.add_argument("--radio", action="store",
                default="http://amber.streamguys.com:4860",
                help="set radio stream URL (default WZBC)")
        self.args = parser.parse_args()
        
        
        # Video recording mode setup:
        if not self.args.nocam:
            from piseccam import cam

            self.cam = cam.PiSecCam()
            self.is_recording = False
            self.longdatestamp = ''
            self.videopath = '/home/pi/Videos'
            if self.args.rotation:
                self.cam.camera.rotation = self.args.rotation

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

            if self.args.nocamdate:
                self.cam.annotate = False

        # Other pin 10 script setup:
        else: self.other10 = False


        # Radio mode setup:
        self.radio_pin = 22
        io.setup(self.radio_pin, io.IN)
        self.is_radio = False
        
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
        if not self.args.nocam:
            if self.is_recording:
                self.cam.stop_cam()
                self.is_recording = False
        elif self.other10:
            subprocess.Popen(['/usr/bin/killall', 'other10.sh'])
            self.other10 = False
        if self.is_radio:
            subprocess.Popen(['/usr/bin/killall', 'mpg123'])
            subprocess.Popen(['/usr/bin/amixer', 'cset',
                'numid=3', '0'])
            self.is_radio = False
        if self.is_wifi:
            subprocess.Popen(['/usr/bin/killall', 'wifi.sh'])
            self.is_wifi = False



    def sigterm_handler(self, signal, frame):
        self.do_stop()
        exit(0)

    

    def do_modes(self):

        while True:
            
            # Video recording mode:
            if not self.args.nocam:
                if io.input(self.cam_pin):
                    if not self.is_recording:
                        self.is_recording = True
                        hscount = 2400
                        if not self.args.nocam:
                            self.longdatestamp = \
                                    datetime.now().strftime('%Y-%m-%d-%H%M%S')
                            self.cam.start_cam(self.longdatestamp + '.h264')
                    else:
                        if hscount == 0:
                            self.longdatestamp = \
                                    datetime.now().strftime('%Y-%m-%d-%H%M%S')
                            self.cam.camera.split_recording(self.longdatestamp + \
                                    '.h264')
                        else:
                            hscount = hscount - 1
                            
                else:
                    if self.is_recording:
                        if self.args.norecstop:
                            if hscount == 0:
                                self.longdatestamp = \
                                        datetime.now().strftime('%Y-%m-%d-%H%M%S')
                                self.cam.camera.split_recording(self.longdatestamp + \
                                        '.h264')
        
                                syslog.syslog(syslog.LOG_INFO,
                                        'Video: Split: ' + self.longdatestamp + \
                                                '.h264')
                                hscount = 1200
                            else:
                                hscount = hscount - 1
                        else:
                            self.cam.stop_cam()
                            self.is_recording = False

            else:
                # Other pin 10 (camera is disabled)
                if io.input(self.cam_pin):
                    subprocess.Popen(['/home/pi/bin/other10.sh'])
                    self.other10 = True
                    


            # Radio mode:
            if io.input(self.radio_pin):
                if not self.is_radio:
                    subprocess.Popen(['/usr/bin/amixer', 'cset',
                        'numid=3', '1'])
                    subprocess.Popen(['/usr/bin/mpg123 ', self.args.radio])
                    self.is_radio = True


            # Wifi mode:
            if io.input(self.wifi_pin):
                if not self.is_wifi:
                    subprocess.Popen(
                            ['/home/pi/src/pisectools/scripts/wifi.sh'])
                    self.is_wifi = True


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
