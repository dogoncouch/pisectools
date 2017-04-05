# LISARD
## Log Intelligent Security Aware Resilient Daemon
LISARD is a security intelligence framework. It is currently in the early stages of development. The end result should be a system that is:

* Aware of its surroundings
* Able to make decisions
* Resilient

## Logging
LISARD relies heavily on the syslog daemon for its sense of awareness and memory. One of the goals is to make use of syslog's robust set of features, and not reinvent the wheel. We are currently using rsyslog for logging.

## Hardware
LISARD is built on Raspberry Pi hardware. It is affordable and efficient, and it can run Linux and rsyslog.

## Software
LISARD currently uses the Raspbian operating system, which is based on Debian Linux, and comes with a lot of well written libraries for Raspberry Pi hardware. Most of our programming is in Python, with scripts and Makefiles for setup and administration tasks.

## Simplicity
One of the goals of this project is to be as simple and understandable as is reasonable.

## Links
* [LISARD framework spec](https://github.com/dogoncouch/lisard/blob/master/framework.txt)
* [rsyslog](http://www.rsyslog.com/)
* [Raspberry Pi Foundation](https://www.raspberrypi.org/)
* [Raspbian](https://www.raspbian.org/)
* [Debian](https://www.debian.org/)
* [Software License](https://github.com/dogoncouch/lisard/blob/master/LICENSE)

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
