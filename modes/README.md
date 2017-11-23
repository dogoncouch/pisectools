# Pi sec tools modes system
## Description
The goal of the modes system is to provide a minimal interface system to a Raspberry Pi. One way communication is achieved by connecting 3.3v outputs to various GPIO input pins.

## Hardware
The modes.py system was developed for Raspberry Pi hardware. It should work with any Raspberry Pi, provided the necessary libraries are installed.

## Required modules
The piseccam module is required, and is also in the repo. Camera support requires the picamera module, and remote recording support requires the paramiko module (python-paramiko).

## Usage

```
usage: modes.py [-h] [--nocam] [--camdate] [--rotation ROTATION] [--fhd]
                [--hd] [--svga] [--vga] [--ld] [--norecstop]

optional arguments:
  -h, --help           show this help message and exit
  --nocam              disable camera support
  --camdate            enable datestamp in camera
  --rotation ROTATION  set camera rotation
  --fhd                enable 1080p video
  --hd                 enable 720p video
  --svga               enable svga video (800x600)
  --vga                enable vga video (640x480)
  --ld                 enable low def video (400x300, 15fps)
  --norecstop          keep recording when jumper is removed
```

Connect GPIO pins to 3.3v power to communicate. Here is the default setup:
- Pin 10: Record video (stops when disconnected)
- Pin 22: Start playing college radio
- Pin 27: Execute wifi script at `/home/pi/bin/wifi.sh`
- Pin 2:  Stop everything
- Pin 24: Shut down

These pins are all reachable with jumpers from nearby 3.3v power pins.

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
