# LISARD modes system
## Goals
The goal of the modes system is to provide a minimal interface system to a Raspberry Pi. One way communication is achieved by connecting 3.3v outputs to various GPIO input pins.

## Hardware
The LISARD modes system was developed for Raspberry Pi hardware. It should work with any Raspberry Pi, provided the necessary libraries are installed.

## Required modules
The lisard module is required, and is also in the repo. Camera support requires the picamera module, and remote recording support requires the paramiko module (python-paramiko).

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
  --svga               enable svga video
  --vga                enable vga video
  --ld                 enable low def video (400x300)
  --norecstop          keep recording when jumper is removed
```

Connect GPIO pins to 3.3v power to communicate. Here is the default setup:
- Pin 10: Record video (stops when disconnected)
- Pin 22: start playing college radio
- Pin 27: execute wifi script
- Pin 2: Stop everything

These pins are all reachable with jumpers from nearby 3.3v power pins.

## Usability
This project is pre-alpha. Documentation is incomplete.

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
