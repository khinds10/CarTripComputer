#! /usr/bin/python
# Car Trip Computer - button manager
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, json
import includes.data as data
from gpiozero import Button
from datetime import datetime
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# setup up button GPIO connections
tripButton = Button(18)

def buttonPress():
    """button pressed, toggle the trip driving/idle time"""
    tripStatus = mc.get("TRIPBUTTON")
    
    # toggle trip status accordingly
    if tripStatus is None:
        mc.set("TRIPBUTTON", str("IDLE"))
    if tripStatus == "DRIVING":
        mc.set("TRIPBUTTON", str("IDLE"))
    if tripStatus == "IDLE":
        mc.set("TRIPBUTTON", str("DRIVING"))
        
while True:
    tripButton.when_pressed = buttonPress
    time.sleep(0.1)
