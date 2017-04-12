#!/usr/bin/env python

from time import sleep, strftime
from datetime import datetime
from picamera import PiCamera, Color
import paramiko


class LisardCam:
    try:
        def __init__(self):
            self.camera = PiCamera()
            self.set_res('fhd')
            self.annotate = False
            self.camera.annotate_background = Color('black')
            self.camera.rotation = 270
            self.is_remote = False
            self.sftp = None
            self.key_file = '/home/pi/.ssh/id_rsa'
            self.output_dir = '/home/pi/Videos'

        
        def set_res(self, res='fhd'):
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

        
        def open_connect(self, user=pi, trustkeys=False, rhost):
            self.is_remote = True
            self.client = paramiko.SSHClient()
            ourkey = paramiko.RSAKey.from_private_key_file(self.key_file)
            self.client.load_system_host_keys()
            if trustkeys:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(rhost, username=user, pkey=ourkey)
            self.sftp = self.client.open_sftp()

        def close_connect(self):
            self.client.close()
            self.is_remote = False
        

        def keep_date(self):
            while True:
                datestamp = datetime.now().strftime('%Y-%m-%d-%H:%M')
                self.camera.annotate_text = datestamp
                sleep(10)
        
        
        def start_cam(self):
            ourdatestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
            filename = self.output_dir + '/' + ourdatestamp + '.h264'
            if self.is_remote == True:
                f = self.sftp.open(filename, 'w')
            else:
                f = filename
            if self.annotate == True:
                # To Do: Start annotation subprocess
                pass
            self.camera.start_recording(f)

        def stop_cam(self):
            self.camera.stop_recording()
            if self.annotate == True:
                # To Do: Kill annotation subprocess
                pass
        
        
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
        
        
    except Exception:
        self.close_connect()

def main():
    cam = LisardCam()
    cam.start_cam()

if __name__ == "__main__":
    cam = LisardCam()
    cam.start_cam()
