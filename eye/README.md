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
  --fullcam            enable non-stop recording
  --nocamdate          disable datestamp in camera
  --rotation ROTATION  set camera rotation
  --fhd                enable 1080p video
  --hd                 enable 720p video
  --svga               enable svga video (800x600)
  --vga                enable vga video (640x480)
  --ld                 enable low def video (400x300) (default)
```

## Basic function
`3.3v` volts on GPIO pin 18 (from a motion sensor) creates a motion event. If the camera is not disabled, it also turns the camera on and creates a camera event. Syslog events are created in the `local2` facility, with severity `info`. When the voltage stops, another motion event is created. The camera turns off, if enabled, with another camera event. Can also be used for door sensors. Notices about the program starting and stopping are sent to the same facility, with `notice` severity.

## Syslog
This system relies heavily on syslog. Gaining a good understanding of how syslog works is essential.

## Remote recording
Remote recording requires an ssh server with RSA key authentication enabled, and a local RSA key on the Pi that is authorized on the server. This creates a known vulnerability: someone with physical access to the Pi could read the private key from the SD card, and get access to the server. We are considering using DMCrypt and LUKS to encrypt the private key in the future.

## Usability
This project is pre-alpha. Documentation is incomplete.

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
