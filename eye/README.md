# LISARD eye system
## Goals
The goal of the eye system is to record events and pass them on to the central system for analyzation. Motion detector events are recorded and passed on using syslog, and optional video is recorded remotely with sftp.

## Hardware
The LISARD eye system was developed on Raspberry Pi hardware using a passive infrared motion sensor, and a Raspberry Pi camera. The camera is optional; running the eye module with the --no-cam option disables camera support.

## Required modules
The lisard module is required, and is also in this repo. Camera support requires the picamera module, and remote recording support requires the paramiko module (python-paramiko).

## Usability
This project is pre-alpha. Documentation is incomplete. Check back in a week or two.

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
