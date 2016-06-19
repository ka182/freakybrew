from bmp183 import bmp183
import requests
import RPi.GPIO as GPIO
import urllib
import json

device_id = 1

url = 'http://46.101.11.33:5000/freakybrew/_temp/%s' % device_id
response = urllib.urlopen(url)
data = json.loads(response.read())

def out_pin():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.OUT)
    GPIO.output(2, GPIO.LOW)

bmp = bmp183()
bmp.measure_pressure()
temperature = bmp.temperature

if data['type'] == 'auto':
    if temperature < 22:
        out_pin()
        status = 'on'
        GPIO.output(2, GPIO.HIGH)
    else:
        out_pin()
        status = 'off'
        GPIO.output(2, GPIO.LOW)

    resp = requests.get('http://46.101.11.33:5000/freakybrew/_device/%s:%s:%s:%s' % (device_id, temperature, data['type'],status))
elif data['type'] == 'manual':
    if data['status'] == 'off':
        out_pin()
        status = 'off'
        GPIO.output(2, GPIO.LOW)
    elif data['status'] == 'on':
        out_pin()
        status = 'on'
        GPIO.output(2, GPIO.HIGH)
    resp = requests.get('http://46.101.11.33:5000/freakybrew/_device/%s:%s:%s:%s' % (device_id, temperature, data['type'],status))