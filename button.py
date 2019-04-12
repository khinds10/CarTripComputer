#! /usr/bin/python
# Car Trip Computer - button manager
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, json
import includes.data as data
from gpiozero import Button
from datetime import datetime

# setup up button GPIO connections
tripButton = Button(18)
def buttonPress():
    """button pressed, toggle the trip driving/idle time"""
    tripStatus = data.getJSONFromFile("driving.json")
    print tripStatus
    
    # toggle trip status accordingly
    if tripStatus == "DRIVING":
        data.saveJSONToFile("driving.json", "IDLE")
    if tripStatus == "IDLE":
        data.saveJSONToFile("driving.json", "DRIVING")

while True:
    tripButton.when_pressed = buttonPress
    time.sleep(0.1)
