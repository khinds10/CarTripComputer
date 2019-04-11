#! /usr/bin/python
# Car Trip Computer - update screen status
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, json
import datetime as dt
import includes.data as data
from gpiozero import Button
from datetime import datetime
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# begin the loop to get the current status to show on the display
while True:

#try:
        # make sure there's no other process using the screen by checking the memcache semaphore variable
        displayInUse = mc.get("INUSE")
        if displayInUse:
            continue
        mc.set("INUSE", True)
    
        # get current date and time
        now = dt.datetime.now()
        timestamp = datetime.timestamp(now)

        # show how long we've been idle or driving for        
        tripStatus = mc.get("TRIPBUTTON")

        # toggle trip status accordingly
        if tripStatus == "DRIVING":
            data.saveJSONToFile('driving.json', 'IDLE')
        if tripStatus == "IDLE":
            data.saveJSONToFile('driving.json', 'DRIVING')
        mc.set("TRIPBUTTON", str(""))

        drivingStatus = getJSONFromFile('driving.json')
        lastUpdate = data.getModificationDate('driving.json')
        lastUpdateReadable = data.displayHumanReadableTime((timestamp-lastUpdate))

        # show driving time
        if drivingStatus == "DRIVING":    
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "189"])
            subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "10", "200", "Driving"])
            subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "40", "230", str(lastUpdateReadable)])

        # show idle time
        if drivingStatus == "IDLE":
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "245"])
            subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "10", "200", "Idle"])
            subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "40", "230", str(lastUpdateReadable)])

        # turn off the in use flag for the screen, we're done writing to it
        mc.set("INUSE", False)

        # wait 1 second
        #time.sleep(1)

    #except (Exception):
    
        # Network or other issue, wait 1 second
        # mc.set("INUSE", False)
        #    time.sleep(1)
