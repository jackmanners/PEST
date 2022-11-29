# PiicoDev-based room sensor...

from dependencies.PiicoDev_SSD1306 import *
from dependencies.PiicoDev_BME280 import *
from dependencies.PiicoDev_VEML6030 import *
from dependencies.PiicoDev_VEML6040 import *
from PiicoDev_Unified import sleep_ms

import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import socket
import json

import micropython
import gc

### SENSOR INITIALIZING ###
atmos = PiicoDev_BME280()
zeroAlt = atmos.altitude() # Initial altitude reading for baseline.

try:
    light = PiicoDev_VEML6030()
except: pass
try:
    color = PiicoDev_VEML6040()
except: pass

display = create_PiicoDev_SSD1306() # Initialise the Display

### WIFI INITIALIZING ###

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = 'Android'
password = '12345678'

# Fill in your network name (ssid) and password here:
wlan.connect(ssid, password)

data_ls = []
block = 1

def check_connection():
    while not wlan.isconnected():
        status = wlan.status()
        display.fill(0)
        display.text("|Pico Sensor|", 0, 0, 1)
        display.text("CHECK NETWORK", 0, 30, 1)
        if status <= 0:
            wlan.connect(ssid, password)
            display.text("Status: DOWN", 0, 40, 1)
        if (status == 1) or (status == 2):
            display.text("Status: JOINING", 0, 40, 1)
        if status == 3:
            display.text("Status: CONNECTED", 0, 40, 1)
        display.show()
        sleep_ms(1000)
            

def show(tempC, humRH, lux, cct):
    display.fill(0)
    display.text("|Pico Sensor|", 0, 0, 1)
    display.text("Temp (C) : "+str(round(tempC, 1)), 0, 20, 1)
    display.text("Hum (%RH): "+str(round(humRH, 1)), 0, 30, 1)
    display.text("Lux (lx) : "+str(round(lux, 1)), 0, 40, 1)
    display.text("CCT (K)  : "+str(int(cct)), 0, 50, 1)
    display.show()
    
    
def to_snapi(data_ls):
    data = json.dumps(data_ls)
    print("\n\nSending to SNAPI:")
    url = "http://www.snapi.space/print"
    r = urequests.post(url, data=data)
    print(r.text)


while True:
    check_connection()

    try:
        r = urequests.get("http://date.jsontest.com")
        time_json = r.json()
        epoch = time_json['milliseconds_since_epoch']
    except OSError as exc:
        if exc == -2:
            print("NETWORK NOT CONNECTED")
            epoch = "UNKNOWN: No network connection"
        else:
            epoch = "UNKNOWN"
               
    tempC, presPa, humRH = atmos.values()
    sleep_ms(1000)
    sleep_ms(1000)
    hsv = color.readHSV()
    rgb = color.readRGB()
    sleep_ms(1000)
    hue = hsv['hue']
    alt = atmos.altitude() - zeroAlt
    sleep_ms(1000)
    data = {
        'epoch_time': epoch,
        'tempC': tempC,
        'pres_hPa': presPa/100,
        'humRH': humRH,
        'lux': light.read(),
        'rgb': rgb,
        'hsv': hsv,
        'alt': alt
    }
    
    data_ls.append(data)
    show(tempC, humRH, light.read(), rgb['cct'])
    block += 1
    
    if block == 6:
        to_snapi(data_ls)
        data_ls=[]
        block=1
        gc.collect()
    
    sleep_ms(1000)

        

    
