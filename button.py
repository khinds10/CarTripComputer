#! /usr/bin/python
# Car Trip Computer - button manager
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, json
import includes.data as data
from gpiozero import Button
from datetime import datetime
mc = memcache.Client(["127.0.0.1:11211"], debug=0)


## GET THIS OUT OF MEMCACHE, JUST HAVE IT SAVE DIRECTLY, IT'S NOT POLLING RIGHT


# setup up button GPIO connections
tripButton = Button(18)
def buttonPress():
    """button pressed, toggle the trip driving/idle time"""
    tripStatus = mc.get("TRIPBUTTON")
    
    # toggle trip status accordingly
    if tripStatus is "":
        mc.set("TRIPBUTTON", "IDLE")
    if tripStatus == "DRIVING":
        mc.set("TRIPBUTTON", "IDLE")
    if tripStatus == "IDLE":
        mc.set("TRIPBUTTON", "DRIVING")
        
    print "button pressed"
    tripStatus = mc.get("TRIPBUTTON")
    print tripStatus

while True:
    tripButton.when_pressed = buttonPress
    time.sleep(0.1)
