import urllib, json
import pprint

import schedule
import time
import datetime

from phue import Bridge # for Philips Hue

import pync # for OS X notifications

# Hue connection stuff
b = Bridge('BRIDGE IP') # Enter bridge IP here.

#If running for the first time, press button on bridge and run with b.connect() uncommented
#b.connect()

# set arrival time
arrivalHour = 9
arrivalMinute = 30

# set addresses and Google Maps API key
mapsDeparture = 'Street+24+City+Country'
mapsDestination = 'Street+42+OtherCity'
mapsKey = 'GOOGLE MAPS API KEY'

def travelTime(): # get travel time with traffic from Google Maps
    mapsurl = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + mapsDeparture + '&destinations=' + mapsDestination + '&departure_time=now&key=' + mapsKey
    googleResponse = urllib.urlopen(mapsurl)
    jsonResponse = json.loads(googleResponse.read())
    #pprint.pprint(jsonResponse)

    travelMinutes = jsonResponse['rows'][0]['elements'][0]['duration_in_traffic']['text']
    travelTime = int(travelMinutes.split()[0])

    return travelTime

def blink(light_id, transTime, blinkTimes): # make HUE light blink red
    # get base values
    baseHue = b.get_light(light_id, 'hue')
    baseSat = b.get_light(light_id, 'sat')
    baseOn = b.get_light(light_id, 'on')

    if baseOn is False: # set light on if it isn't already
        b.set_light(light_id, 'on', True)

    # make it red
    b.set_light(light_id, 'hue', 0)
    b.set_light(light_id, 'sat', 255)

    # blink!
    for i in range(0,blinkTimes):
        b.set_light(light_id, 'bri', 200, transitiontime=transTime)
        time.sleep(0.3)
        b.set_light(light_id, 'bri', 0, transitiontime=transTime)
        time.sleep(0.5)

    # set back to original color
    b.set_light(light_id, 'hue', baseHue)
    b.set_light(light_id, 'sat', baseSat)

    if baseOn is False: # turn light back off if it was off
        b.set_light(light_id, 'on', False)

today = datetime.datetime.now()
todayArrival = today.replace(hour=arrivalHour, minute=arrivalMinute, second=0, microsecond=0)

def timeToGo():
    global today
    global todayArrival
#   if todayArrival.day == today.day:
    # get estimated arrival time: current time + travel time minutes + 10 minutes
    estTime = datetime.datetime.now() + datetime.timedelta(minutes=travelTime() + 10)
    # print estTime

    if estTime > todayArrival:  # if it's time to go
        # print 'its wooooorkiiiiing!'
        pync.notify('You must leave now if you want to arrive at '
                    + str(arrivalHour) + ':' + str(arrivalMinute)
                    + '. Current travel time is ' + str(travelTime())
                    + ' minutes.', title='Time to leave')
        blink(1,5,5)
        todayArrival = todayArrival.replace(day=todayArrival.day+1) # don't run again today

schedule.every(10).seconds.do(timeToGo)

while True:
    schedule.run_pending()
    time.sleep(1)
