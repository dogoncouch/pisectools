# LISARD
## Log Intelligent Security Aware Resilient Daemon
LISARD is a security intelligence framework. It is currently in the early stages of development. The end result should be a system that is:

* Aware of its surroundings
* Able to make decisions
* Resilient

## Logging
LISARD relies heavily on the syslog daemon for its sense of awareness and memory. One of the goals is to make use of syslog's robust set of features, and not reinvent the wheel. We are currently using rsyslog for logging, but plan on adding support for syslog-ng.

## Hardware
LISARD is built on Raspberry Pi hardware. Here are a few of the reasons:

* It is affordable
* It is efficient
* It can run Linux and syslog
* It comes with programmable inputs and outputs
* It is well supported

## Software
LISARD currently uses the Raspbian operating system, which is based on Debian Linux, and comes with a lot of well written libraries for Raspberry Pi hardware. Most of our programming is in Python, with shell scripts and Makefiles for setup and administrative tasks.

## Simplicity
One of the goals of this project is to be as simple and understandable as is reasonable.

## Links

### Working Software
Each has its own README.md.
* [LISARD eye system](eye/)
* [LISARD 'modes' input system](modes/)

### Libraries
* [LISARD main library](lisard/)

### Project Information
* [LISARD framework spec](https://github.com/dogoncouch/lisard/blob/master/doc/framework.txt)
* [Software License](https://github.com/dogoncouch/lisard/blob/master/LICENSE)

### External Resources
* [rsyslog](http://www.rsyslog.com/)
* [Raspberry Pi Foundation](https://www.raspberrypi.org/)
* [Raspbian](https://www.raspbian.org/)
* [Debian](https://www.debian.org/)

(c) 2017 Dan Persons ([dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com))
