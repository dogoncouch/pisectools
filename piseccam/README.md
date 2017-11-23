# Pi sec tools: piseccam module
## Description
Raspberry Pi security camera module, made to simplify basic functionality for the Raspberry Pi camera.

## Required modules
Camera support requires the picamera module, and remote recording support requires the paramiko module (python-paramiko).

## Usage
Camera object initialization:

    cam = piseccam.PiSecCam()

Available resolutions: `'fhd'` (1080p), `'hd'` (720p), `'svga'` (800x600), `'vga'` (640x480), `'ld'` (400x300). Set resolution:

    cam.set_res(res='svga')

Remote recording setup:

    cam.is_remote = True
    cam.open_connect(REMOTEHOST[, user=USERNAME, keyfile=KEYFILE, trustkeys=True])

Disable remote recording:

    cam.is_remote = False
    cam.close_connect()

Start/split/stop recording:

    cam.start_cam(FILENAME)
    cam.split_cam(FILENAME)
    cam.stop_cam()

Cycle through effects:

    cam.cycle_effects()

Change camera rotation:

    cam.camera.rotation = 90 | 180 | 270

Note: PiCamera object can be accessed directly via `cam.camera`.

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
