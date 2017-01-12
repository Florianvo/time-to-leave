# time-to-leave
Python script that makes Philips Hue light blink if it's time to go to (by checking Google Maps travel time)

## Dependencies
I use a few Python modules to get this script working:
* pync for OS X notifications: https://github.com/SeTeM/pync
* phue for Philips Hue control: https://github.com/studioimaginaire/phue
* schedule to check periodically: https://github.com/dbader/schedule

In order to get the 'time in traffic' from Google Maps you'll need to get a (free) API key [over here](https://console.developers.google.com/projectselector/apis/credentials).
