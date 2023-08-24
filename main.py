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

### TIME SETTINGS ###
measurement_interval = 10 # Seconds

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


def to_snapi(token, data):    
    url = "http://www.snapi.space/api/pest/upload"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+token}
    
    r = urequests.post(url, headers=headers, data=data)
    
def avg(list):
    avg = sum(list)/len(list)
    return round(avg, 2)


def adjust_measurement_interval():
    current_time = utime.localtime()
    minutes = current_time[4]
    seconds = current_time[5]
    seconds_until_next_interval = measurement_interval - (minutes % 10) * 60 - seconds

    utime.sleep(seconds_until_next_interval)


def adjust_coefficients_by_cct(cct):
    if cct < 3000:
        return {
            "red": 0.1,
            "green": 0.2,
            "blue": 0.6
        }
    elif cct < 5000:
        return {
            "red": 0.1,
            "green": 0.3,
            "blue": 0.5
        }
    else:
        return {
            "red": 0.1,
            "green": 0.3,
            "blue": 0.4
        }

def calculate_melanopic_lux(data):
    melanopic_coefficients = adjust_coefficients_by_cct(data["cct"])
    
    w_red = data["red"] * melanopic_coefficients["red"]
    w_green = data["green"] * melanopic_coefficients["green"]
    w_blue = data["blue"] * melanopic_coefficients["blue"]
    
    melanopic_value = (w_red + w_green + w_blue)
    total_rgbw_sum = data["red"] + data["green"] + data["blue"]
    
    relative_melanopic_value  = melanopic_value / total_rgbw_sum if total_rgbw_sum != 0 else 0

    # Scale by overall illuminance (ALS)
    melanopic_lux = relative_melanopic_value * data["white"]

    return melanopic_lux

### MAIN PROGRAM ###
check_connection()
token = token()

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
    
    rgb = sensor.color.readRGB()
    melanopic_lux = calculate_melanopic_lux(rgb)

    data = {
        "pest_id": "jack_pest",
        "recording_id": "recording_1",
        "data": {
            "rgb": rgb,
            "melanopic_lux_estimate": melanopic_lux
        }
    }
    
    data = json.dumps(data)
    to_snapi(token, data)
    
    time_diff = utime.ticks_diff(utime.ticks_ms(), starttime)/1000
    adjust_measurement_interval()
    utime.sleep(measurement_interval - time_diff)
    data = None
    gc.collect()