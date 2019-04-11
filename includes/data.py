#! /usr/bin/python
# Data helper functions to save and load application values on the file system
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, os, datetime

def getJSONFromFile(fileName):
    """get JSON contents from file in question"""
    try:
        with open('/home/pi/CarTripComputer/data/' + filename) as dataFile:    
            return json.load(dataFile)
    except (Exception):
        return ""

def saveJSONToFile(filename, JSONData):
    """save data to file"""
    f = file('/home/pi/CarTripComputer/data/' + filename, "w")
    f.write(str(json.dumps(JSONData)))

def displayHumanReadableTime(seconds, granularity=3):
    """display human readable units of time for given seconds"""
    intervals = (('d', 86400),('h', 3600),('m', 60),)
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(value, name))
    return ''.join(result[:granularity])

def getModificationDate(filename):
    """get last modification date for file"""
    return os.path.getmtime('/home/pi/CarTripComputer/data/' + filename)
    
