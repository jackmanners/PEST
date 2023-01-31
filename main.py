# PiicoDev-based room sensor...
from PiicoDev_Unified import sleep_ms
from device_config import pico_sensors, pest_id, wifiSetup, lab_id

import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import socket
import json
from network import WLAN

import micropython
import gc
import utime
from ucollections import OrderedDict

sensor = pico_sensors()
sensor.test_sensors()

### WIFI INITIALIZING ###
ssid = wifiSetup().android_ssid
password = wifiSetup().android_password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(ssid, password)
gc.collect()

def check_connection():
    while not wlan.isconnected():
        status = wlan.status()
        if status <= 0:
            wlan.connect(ssid, password)
            print("DOWN")
        if (status == 1) or (status == 2):
            print("JOINING")
        if status == 3:
            print("CONNECTED")
        utime.sleep(1)


def token():
    url = "http://www.snapi.space/api/tokens"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic amFjay5tYW5uZXJzQGZsaW5kZXJzLmVkdS5hdTpaYXExTWprbA=="}
    r = urequests.post(url, headers=headers).json()

    return r['access_token']


def to_snapi(data):   
    url = "http://www.snapi.space/api/participant/{}/pest/receive".format(lab_id)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+token()}
    
    r = urequests.post(url, headers=headers, data=data)
    status = r.text


def avg(list):
    avg = sum(list)/len(list)
    return round(avg, 2)


### MAIN PROGRAM ###
check_connection()

while True:
    ## Re-define data ##
    datetime_ls = []
    precisionTemp_ls = []
    pres_hPa_ls = []
    humRH_ls = []
    lux_ls = []
    cct_ls = []
    data = None
    minuteData = None
    
    gc.collect()
    
    ## Collect sensor data for n times before sending ##
    starttime = utime.ticks_ms()
    try:
        r = urequests.get("http://date.jsontest.com")
        time_json = r.json()
        epoch = time_json['milliseconds_since_epoch']
        datetime = epoch
    except OSError as exc:
        print("NETWORK NOT CONNECTED")
        datetime = utime.time()*1000
    
    tempC, presPa, humRH = sensor.atmos.values()
    rgb = sensor.color.readRGB()
    precisionTemp = sensor.temp.readTempC()
    lux = sensor.light.read()
    
    ## Runs after collecting 10 chunks of data ##
    data = OrderedDict([
        ("pest_id", pest_id),
        ("epochtime", datetime),
        ("temp", precisionTemp),
        ("pres_hPa", presPa/100),
        ("humRh", humRH),
        ("lux", lux),
        ("cct", rgb["cct"])
    ])
    
    data = json.dumps(data)
    to_snapi(data)
    time_diff = utime.ticks_diff(utime.ticks_ms(), starttime)/1000       
    utime.sleep(5*60-time_diff)
    gc.collect()
