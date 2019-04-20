#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import datetime as dt
import time, json, string, cgi, subprocess, json, memcache
import settings as settings
import Adafruit_DHT
mc = memcache.Client(["127.0.0.1:11211"], debug=0)

# Raspberry Pi with DHT sensor - connected to GPIO16 / Pin 36
sensor = Adafruit_DHT.DHT22
pin = 17

def showHourlyColorCodes(hourlyConditions):
    stepCount = 22
    currentStep = 10
    for hourlyMeasurement in hourlyConditions:
        subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "5"])
        if hourlyMeasurement["icon"] == "clear-day":
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "42"])
        if hourlyMeasurement["icon"] == "clear-night":
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "42"])
        if hourlyMeasurement["icon"] == "rain":
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "7"])
        if hourlyMeasurement["icon"] == "sleet":
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "7"])
        if hourlyMeasurement["icon"] == "snow":
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "7"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "drawBox", str(currentStep), "120", "20", "20"])
        currentStep = currentStep + stepCount

# begin the loop to get the current weather for display
mc.set("INUSE", "")
while True:

    try:    
        # make sure there"s no other process using the screen by checking the memcache semaphore variable
        displayInUse = mc.get("INUSE")
        if displayInUse == "INUSE":
            print "display in use"
            time.sleep(1)
            continue
        mc.set("INUSE", "INUSE")
    
        # get current date and time
        date = dt.datetime.now()
        clockValue = date.strftime("%I:%M%p")

        # get 10 readings and average, in case the humidistat is inaccurate
        count, readingCount, avgTemperature, avgHumidity = [ 0, 0, 0, 0 ]
        while (count < 1):    
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None:
                avgTemperature = avgTemperature + temperature
                avgHumidity = avgHumidity + humidity
                readingCount = readingCount + 1                
            count = count + 1
        avgTemperature = avgTemperature / readingCount
        insideTemperature = int(avgTemperature * 9/5 + 32)
        avgHumidity = avgHumidity / readingCount
        insideHumidity = int(avgHumidity)
        
        # get current forecast from location
        weatherInfo = json.loads(subprocess.check_output(["curl", settings.weatherAPIURL + settings.weatherAPIKey + "/" + str(settings.latitude) + "," + str(settings.longitude) + "?lang=en"]))
        currentConditions = weatherInfo["currently"]
        hourlyConditions = weatherInfo["hourly"]        
        icon = str(currentConditions["icon"])
        apparentTemperature = str(int(currentConditions["apparentTemperature"]))
        humidity = str(int(currentConditions["humidity"] * 100))
        windSpeed = str(int(currentConditions["windSpeed"]))
        cloudCover = str(int(currentConditions["cloudCover"] * 100))
        precipProbability = str(int(currentConditions["precipProbability"] * 100))

        # minutely conditions, limit the characters to 30 in the summary
        minutelyConditions = weatherInfo["minutely"]
        summary = str(minutelyConditions["summary"])
        summary = (summary[:67] + "...") if len(summary) > 69 else summary

        # hourly conditions, limit the characters to 30 in the summary
        hourlyConditions = weatherInfo["hourly"]
        hourlySummary = str(hourlyConditions["summary"])
        hourlySummary = (hourlySummary[:37] + "...") if len(hourlySummary) > 39 else hourlySummary

        # conditions for the day
        dailyConditions = weatherInfo["daily"]
        dailyConditions = dailyConditions["data"][0]
        apparentTemperatureMin = str(int(dailyConditions["apparentTemperatureMin"]))
        apparentTemperatureMax = str(int(dailyConditions["apparentTemperatureMax"]))
        
        # clear and setup display to show basic info
        subprocess.call(["/home/pi/CarTripComputer/digole", "clear"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "setRot270"])
        subprocess.call(["/home/pi/CarTripComputer/digole", icon])
        subprocess.call(["/home/pi/CarTripComputer/digole", "setFont", "18"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "255"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "10", "95", summary])
        subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "10", "165", hourlySummary])
        subprocess.call(["/home/pi/CarTripComputer/digole", "setFont", "18"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "80", "20", date.strftime("%a, %b %d")])
        
        # show upcoming conditions as color coded blocks by hour        
        showHourlyColorCodes(hourlyConditions["data"][0:10])

        # print the min daily temp in the evening and night, print the day max temp in the morning and daytime
        if dt.datetime.now().hour > 16 or dt.datetime.now().hour < 6:
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "27"])
            subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "90", "45", "LOW\n" + apparentTemperatureMin + "*F"])
        else:
            subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "240"])
            subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "90", "45", "HIGH\n" + apparentTemperatureMax + "*F"])
        
        # show outdoor temp
        subprocess.call(["/home/pi/CarTripComputer/digole", "setFont", "51"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "255"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "240", "40", apparentTemperature + "*F [" + humidity + "%]"])
        
        # show clock value
        subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "253"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "250", "75", str(clockValue)])
        
        # show indoor temp
        subprocess.call(["/home/pi/CarTripComputer/digole", "setColor", "250"])
        subprocess.call(["/home/pi/CarTripComputer/digole", "printxy_abs", "190", "230", "IN: " + str(insideTemperature) + "* F [" + str(insideHumidity) + " %]"])

        # turn off the in use flag for the screen, we"re done writing to it
        mc.set("INUSE", "")

        # wait 1 minute
        time.sleep(60)

    except (Exception):
        # Network or other issue, wait 1 minute
        mc.set("INUSE", "")
        time.sleep(60)
