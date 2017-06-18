# LISARD eye system
## Goals
The goal of the eye system is to record events and pass them on to the central system for analyzation. Motion detector events are recorded and passed on using syslog, and optional video is recorded remotely with sftp.

## Hardware
The LISARD eye system was developed on Raspberry Pi hardware using a passive infrared motion sensor, and a Raspberry Pi camera. The camera is optional; running the eye module with the --nocam option disables camera support.

## Required modules
The lisard module is required, and is also in this repo. Camera support requires the picamera module, and remote recording support requires the paramiko module (python-paramiko).

## Usage

```
usage: eye.py [-h] [--remote REMOTE] [--trusthostkeys] [--nocam] [--nocamdate]
              [--rotation ROTATION] [--fhd] [--hd] [--svga] [--vga] [--ld]

optional arguments:
  -h, --help           show this help message and exit
  --remote REMOTE      set remote host for video files
  --trusthostkeys      auto-add remote host keys (use with caution
  --nocam              disable camera support
  --nocamdate          disable datestamp in camera
  --rotation ROTATION  set camera rotation
  --fhd                enable 1080p video
  --hd                 enable 720p video
  --svga               enable svga video (800x600)
  --vga                enable vga video (640x480)
  --ld                 enable low def video (400x300) (default)
```

`3.3v` volts on GPIO pin 18 (from a motion sensor) turns the camera on and creates a syslog event. Camera turns off (with another syslog event) when the voltage stops.

## Usability
This project is pre-alpha. Documentation is incomplete.

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
