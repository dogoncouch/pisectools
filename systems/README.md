# LISARD Core Systems
## lisard\_eye.py
 `` lisard_eye.py `` provides log intelligence for physical security environments. It creates syslog events based on input from a passive infrared motion sensor, and records video when motion is detected (video is optional).
 
 `` lisard_eye.py `` was designed to use a passive infrared motion sensor that outputs 3.3v when engaged, connected to GPIO pin 18 on the Raspberry Pi. The prototype was made using a [PIR motion sensor from Adafruit](https://www.adafruit.com/products/189), but it should work with any PIR motion sensor that outputs 3.3v.

## lisard\_motion.py
 `` lisard_motion.py `` is deprecated in favor of `` lisard_eye.py `` , but is still available for reference. It does not record video, but you can get the same effect using `` lisard_eye.py `` as follows:

    python lisard_eye.py --no-cam

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
