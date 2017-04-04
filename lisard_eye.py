#!/usr/bin/env python

import time
import RPi.GPIO as io
io.setmode(io.BCM)
import syslog

syslog.openlog(facility=syslog.LOG_LOCAL2)
# syslog.openlog(ident="Motion", logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL2)
pir_pin = 18

io.setup(pir_pin, io.IN)
ismotion = False
idlecount = 40

while True:
    if io.input(pir_pin):
        if not ismotion:
            syslog.syslog(syslog.LOG_INFO, "Motion detected")
            ismotion = True
    else:
        if ismotion:
            syslog.syslog(syslog.LOG_INFO, "Motion stopped")
            ismotion = False
    time.sleep(0.5)
